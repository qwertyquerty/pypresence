import asyncio
import inspect
import json
import logging
import os
import struct
import sys
import tempfile
from typing import Union, Optional, Callable

# TODO: Get rid of this import * lol
from .exceptions import *
from .payloads import Payload
from .utils import get_ipc_path, get_event_loop


class BaseClient:

    def __init__(self, client_id: str, **kwargs):
        loop: Optional[asyncio.AbstractEventLoop] = kwargs.get('loop', None)
        handler: Optional[Callable] = kwargs.get('handler', None)
        self.pipe: Optional[int] = kwargs.get('pipe', None)
        self.isasync: bool = kwargs.get('isasync', False)
        self.connection_timeout: int = kwargs.get('connection_timeout', 30)
        self.response_timeout: int = kwargs.get('response_timeout', 10)

        client_id = str(client_id)

        if loop is not None:
            self.update_event_loop(loop)
        else:
            self.update_event_loop(get_event_loop())

        self.sock_reader: Optional[asyncio.StreamReader] = None
        self.sock_writer: Optional[asyncio.StreamWriter] = None
        self.loop: asyncio.AbstractEventLoop
        self.handler: Optional[Callable] = None
        self._events_on: bool

        self.client_id: str = client_id

        if handler is not None:
            if not inspect.isfunction(handler):
                raise PyPresenceException('Error handler must be a function.')
            args = inspect.getfullargspec(handler).args
            if args[0] == 'self':
                args = args[1:]
            if len(args) != 2:
                raise PyPresenceException('Error handler should only accept two arguments.')

            if self.isasync:
                if not inspect.iscoroutinefunction(handler):
                    raise InvalidArgument('Coroutine', 'Subroutine', 'You are running async mode - '
                                                                     'your error handler should be awaitable.')
                err_handler = self._async_err_handle
            else:
                err_handler = self._err_handle

            self.loop.set_exception_handler(err_handler)
            self.handler = handler

        if getattr(self, "on_event", None):  # Tasty bad code ;^)
            self._events_on = True
        else:
            self._events_on = False

    def update_event_loop(self, loop: asyncio.AbstractEventLoop) -> None:
        # noinspection PyAttributeOutsideInit
        self.loop = loop
        asyncio.set_event_loop(self.loop)

    def _err_handle(self, loop: asyncio.AbstractEventLoop, context: dict) -> None:
        result = self.handler(context['exception'], context['future'])
        if inspect.iscoroutinefunction(self.handler):
            loop.run_until_complete(result)

    # noinspection PyUnusedLocal
    async def _async_err_handle(self, loop: asyncio.AbstractEventLoop, context: dict) -> None:
        await self.handler(context['exception'], context['future'])

    async def read_output(self) -> dict:
        try:
            preamble = await asyncio.wait_for(self.sock_reader.read(8), self.response_timeout)
            status_code, length = struct.unpack('<II', preamble[:8])
            data = await asyncio.wait_for(self.sock_reader.read(length), self.response_timeout)
        except (BrokenPipeError, struct.error):
            raise PipeClosed
        except asyncio.TimeoutError:
            raise ResponseTimeout
        payload = json.loads(data.decode('utf-8'))
        if payload["evt"] == "ERROR":
            raise ServerError(payload['data']['message'])
        return payload

    def send_data(self, op: int, payload: Union[dict, Payload]) -> None:
        if isinstance(payload, Payload):
            payload = payload.data
        payload = json.dumps(payload)

        if self.sock_writer is None:
            raise ConnectionError("Not connected to Discord. Call connect() first.")

        self.sock_writer.write(
            struct.pack(
                '<II',
                op,
                len(payload)) +
            payload.encode('utf-8'))

    def is_discord_available(self):
        """
        Check if Discord is available without establishing a full connection.
        
        Returns:
            bool: True if Discord appears to be running and available, False otherwise.
        """
        try:
            ipc_path = get_ipc_path(self.pipe)
            if not ipc_path:
                return False
                
            # Check if the IPC pipe exists
            if sys.platform == 'linux' or sys.platform == 'darwin':
                return os.path.exists(ipc_path)
            elif sys.platform == 'win32':
                # On Windows, check if any Discord IPC pipe exists
                for i in range(10):  # Check pipes 0-9
                    pipe_path = rf'\\.\pipe\discord-ipc-{i}'
                    try:
                        os.stat(pipe_path)
                        return True
                    except OSError:
                        continue
                return False
            return False
        except (OSError, PermissionError, ValueError) as e:
            logging.debug(f"Error checking Discord availability: {e}")
            return False

    async def handshake(self) -> None:
        ipc_path = get_ipc_path(self.pipe)
        if not ipc_path:
            raise DiscordNotFound("Could not find Discord IPC path")

        try:
            if sys.platform == 'linux' or sys.platform == 'darwin':
                self.sock_reader, self.sock_writer = await asyncio.wait_for(
                    asyncio.open_unix_connection(ipc_path), 
                    self.connection_timeout
                )
            elif sys.platform == 'win32':
                self.sock_reader = asyncio.StreamReader(loop=self.loop)
                reader_protocol = asyncio.StreamReaderProtocol(self.sock_reader, loop=self.loop)
                self.sock_writer, _ = await asyncio.wait_for(
                    self.loop.create_pipe_connection(lambda: reader_protocol, ipc_path),
                    self.connection_timeout
                )
        except FileNotFoundError:
            raise InvalidPipe("Discord IPC pipe not found")
        except asyncio.TimeoutError:
            raise ConnectionTimeout("Connection to Discord timed out")
        except ConnectionRefusedError:
            raise DiscordNotFound("Discord is running but not accepting connections")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Discord: {e}")

        try:
            self.send_data(0, {'v': 1, 'client_id': self.client_id})
            preamble = await asyncio.wait_for(self.sock_reader.read(8), self.response_timeout)
            code, length = struct.unpack('<ii', preamble)
            data = json.loads(await asyncio.wait_for(self.sock_reader.read(length), self.response_timeout))
            if 'code' in data:
                if data['message'] == 'Invalid Client ID':
                    raise InvalidID("Invalid Discord application ID")
                raise DiscordError(data['code'], data['message'])
            if self._events_on:
                self.sock_reader.feed_data = self.on_event
        except asyncio.TimeoutError:
            # Clean up the connection if handshake times out
            await self.close()
            raise ResponseTimeout("Handshake timed out")
        except Exception as e:
            # Clean up the connection if handshake fails
            await self.close()
            raise e

    async def close(self) -> None:
        """Safely close the connection to Discord"""
        try:
            if self.sock_writer:
                self.sock_writer.close()
                await self.sock_writer.wait_closed()
        except (ConnectionError, OSError, asyncio.CancelledError) as e:
            logging.debug(f"Error during connection cleanup: {e}")
        finally:
            self.sock_reader = None
            self.sock_writer = None

    def try_connect(self):
        """
        Attempt to connect to Discord but don't raise exceptions.
        
        Returns:
            bool: True if connection was successful, False otherwise.
        """
        try:
            self.loop.run_until_complete(self.handshake())
            return True
        except (DiscordNotFound, InvalidPipe, ConnectionTimeout, InvalidID, DiscordError, ConnectionError) as e:
            logging.debug(f"Expected connection failure: {e}")
            return False
        except Exception as e:
            logging.debug(f"Unexpected error during connection attempt: {e}")
            return False
