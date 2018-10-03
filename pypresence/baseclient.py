import inspect
import json
import os
import struct
import sys
import tempfile

from .exceptions import *
from .utils import *
from .response import Response


class BaseClient:

    def __init__(self, client_id, **kwargs):
        pipe = kwargs.get('pipe', 0)
        loop = kwargs.get('loop', None)
        handler = kwargs.get('handler', None)

        client_id = str(client_id)
        if sys.platform == 'linux' or sys.platform == 'darwin':
            self.ipc_path = (
                (os.environ.get('XDG_RUNTIME_DIR') or tempfile.gettempdir())
                + '/discord-ipc-' + str(pipe))
            self.loop = asyncio.get_event_loop()
        elif sys.platform == 'win32':
            self.ipc_path = r'\\?\pipe\discord-ipc-' + str(pipe)
            self.loop = asyncio.ProactorEventLoop()

        if loop is not None:
            self.loop = loop

        self.sock_reader: asyncio.StreamReader = None
        self.sock_writer: asyncio.StreamWriter = None
        self.client_id = client_id

        if handler is not None:
            if not inspect.isfunction(handler):
                raise PyPresenceException('Error handler must be a function.')
            args = inspect.getfullargspec(handler).args
            if args[0] == 'self': args = args[1:]
            if len(args) != 2:
                raise PyPresenceException('Error handler should only accept two arguments.')

            loop.set_exception_handler(self._err_handle)
            self.handler = handler

        if getattr(self, "on_event", None):  # Tasty bad code ;^)
            self._events_on = True
        else:
            self._events_on = False

    def _err_handle(self, loop, context):
        result = self.handler(context['exception'], context['future'])
        if inspect.iscoroutinefunction(self.handler):
            loop.run_until_complete(result)

    async def read_output(self):
        try:
            data = await self.sock_reader.read(1024)
        except BrokenPipeError:
            raise InvalidID
        code, length = struct.unpack('<II', data[:8])
        payload = json.loads(data[8:].decode('utf-8'))
        if payload["evt"] == "ERROR":
            raise ServerError(payload["data"]["message"])
        return Response.from_dict(payload, code=code)

    def send_data(self, op: int, payload: dict):
        payload = json.dumps(payload)
        self.sock_writer.write(
            struct.pack(
                '<II',
                op,
                len(payload)) +
            payload.encode('utf-8'))

    async def handshake(self):
        if sys.platform == 'linux' or sys.platform == 'darwin':
            self.sock_reader, self.sock_writer = await asyncio.open_unix_connection(self.ipc_path, loop=self.loop)
        elif sys.platform == 'win32' or sys.platform == 'win64':
            self.sock_reader = asyncio.StreamReader(loop=self.loop)
            reader_protocol = asyncio.StreamReaderProtocol(
                self.sock_reader, loop=self.loop)
            try:
                self.sock_writer, _ = await self.loop.create_pipe_connection(lambda: reader_protocol, self.ipc_path)
            except FileNotFoundError:
                raise InvalidPipe
        self.send_data(0, {'v': 1, 'client_id': self.client_id})
        data = await self.sock_reader.read(1024)
        code, length = struct.unpack('<ii', data[:8])
        if self._events_on:
            self.sock_reader.feed_data = self.on_event
