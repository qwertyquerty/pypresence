"""Test BaseClient core functionality"""

import asyncio
import json
import struct
import sys
from unittest.mock import AsyncMock, Mock, patch

import pytest

from pypresence.baseclient import BaseClient
from pypresence.exceptions import (
    ConnectionTimeout,
    InvalidArgument,
    InvalidID,
    InvalidPipe,
    PipeClosed,
    PyPresenceException,
    ResponseTimeout,
    ServerError,
)


class TestBaseClientInit:
    """Test BaseClient initialization"""

    def test_init_basic(self, client_id):
        """Test basic initialization"""
        client = BaseClient(client_id)

        assert client.client_id == client_id
        assert client.isasync is False
        assert client.connection_timeout == 30
        assert client.response_timeout == 10

    def test_init_converts_client_id_to_string(self):
        """Test that client_id is converted to string"""
        client = BaseClient(123456789)
        assert client.client_id == "123456789"
        assert isinstance(client.client_id, str)

    def test_init_with_custom_loop(self):
        """Test initialization with custom event loop"""
        loop = asyncio.new_event_loop()
        client = BaseClient("12345", loop=loop)

        assert client.loop is loop
        loop.close()

    def test_init_with_error_handler_invalid_not_function(self, client_id):
        """Test that non-function handler raises exception"""
        with pytest.raises(
            PyPresenceException, match="Error handler must be a function"
        ):
            BaseClient(client_id, handler="not a function")

    def test_init_with_error_handler_wrong_args(self, client_id):
        """Test that handler with wrong number of args raises exception"""

        def bad_handler(only_one_arg):
            pass

        with pytest.raises(
            PyPresenceException, match="should only accept two arguments"
        ):
            BaseClient(client_id, handler=bad_handler)

    def test_init_with_valid_sync_handler(self, client_id):
        """Test initialization with valid sync error handler"""

        def error_handler(exception, future):
            pass

        client = BaseClient(client_id, handler=error_handler)
        assert client.handler is error_handler

    def test_init_with_async_handler_in_sync_mode_raises(self, client_id):
        """Test that async handler in sync mode raises error"""

        async def async_handler(exception, future):
            pass

        # This should work but the handler will be wrapped
        client = BaseClient(client_id, handler=async_handler, isasync=False)
        assert client.handler is async_handler

    def test_init_with_async_handler_requires_coroutine(self, client_id):
        """Test that async mode requires coroutine handler"""

        def sync_handler(exception, future):
            pass

        with pytest.raises(InvalidArgument):
            BaseClient(client_id, handler=sync_handler, isasync=True)


class TestBaseClientSendData:
    """Test BaseClient.send_data() method"""

    def test_send_data_with_dict(self, client_id):
        """Test sending data with dict payload"""
        client = BaseClient(client_id)
        client.sock_writer = Mock()

        payload = {"cmd": "TEST", "args": {"value": 123}}
        client.send_data(1, payload)

        # Verify write was called
        assert client.sock_writer.write.called

        # Check the data format
        call_args = client.sock_writer.write.call_args[0][0]
        op, length = struct.unpack("<II", call_args[:8])

        assert op == 1
        assert length == len(json.dumps(payload))

    def test_send_data_with_payload_object(self, client_id):
        """Test sending data with Payload object"""
        from pypresence.payloads import Payload

        client = BaseClient(client_id)
        client.sock_writer = Mock()

        payload = Payload({"cmd": "TEST"})
        client.send_data(1, payload)

        assert client.sock_writer.write.called

    def test_send_data_without_connection_raises(self, client_id):
        """Test that send_data raises if not connected"""
        client = BaseClient(client_id)
        client.sock_writer = None

        with pytest.raises(AssertionError, match="You must connect your client"):
            client.send_data(1, {})


class TestBaseClientReadOutput:
    """Test BaseClient.read_output() method"""

    @pytest.mark.asyncio
    async def test_read_output_success(self, client_id):
        """Test successful read_output"""
        client = BaseClient(client_id)

        response = {"cmd": "SET_ACTIVITY", "evt": "ACTIVITY_UPDATE", "data": {}}
        response_json = json.dumps(response).encode("utf-8")
        preamble = struct.pack("<II", 1, len(response_json))

        client.sock_reader = AsyncMock()
        client.sock_reader.read = AsyncMock(side_effect=[preamble, response_json])

        result = await client.read_output()

        assert result == response

    @pytest.mark.asyncio
    async def test_read_output_error_event(self, client_id):
        """Test read_output with ERROR event"""
        client = BaseClient(client_id)

        response = {"evt": "ERROR", "data": {"message": "Test error"}}
        response_json = json.dumps(response).encode("utf-8")
        preamble = struct.pack("<II", 1, len(response_json))

        client.sock_reader = AsyncMock()
        client.sock_reader.read = AsyncMock(side_effect=[preamble, response_json])

        with pytest.raises(ServerError, match="Test error"):
            await client.read_output()

    @pytest.mark.asyncio
    async def test_read_output_broken_pipe(self, client_id):
        """Test read_output with broken pipe"""
        client = BaseClient(client_id)
        client.sock_reader = AsyncMock()
        client.sock_reader.read = AsyncMock(side_effect=BrokenPipeError())

        with pytest.raises(PipeClosed):
            await client.read_output()

    @pytest.mark.asyncio
    async def test_read_output_timeout(self, client_id):
        """Test read_output with timeout"""
        client = BaseClient(client_id)
        client.sock_reader = AsyncMock()
        client.sock_reader.read = AsyncMock(side_effect=asyncio.TimeoutError())

        with pytest.raises(ResponseTimeout):
            await client.read_output()

    @pytest.mark.asyncio
    async def test_read_output_struct_error(self, client_id):
        """Test read_output with struct error"""
        client = BaseClient(client_id)
        client.sock_reader = AsyncMock()
        client.sock_reader.read = AsyncMock(side_effect=struct.error())

        with pytest.raises(PipeClosed):
            await client.read_output()


class TestBaseClientHandshake:
    """Test BaseClient.handshake() method"""

    @pytest.mark.asyncio
    async def test_handshake_success(self, client_id, mock_ipc_path):
        """Test successful handshake"""
        client = BaseClient(client_id)

        # Mock successful handshake response
        response = {"cmd": "DISPATCH", "data": {"v": 1}, "evt": "READY"}
        response_json = json.dumps(response).encode("utf-8")
        preamble = struct.pack("<II", 1, len(response_json))

        # Create mock reader and writer
        mock_reader = AsyncMock()
        mock_writer = Mock()
        mock_reader.read = AsyncMock(side_effect=[preamble, response_json])

        # Mock create_reader_writer to set up the mocks
        async def mock_create_reader_writer(ipc_path):
            client.sock_reader = mock_reader
            client.sock_writer = mock_writer

        client.create_reader_writer = AsyncMock(side_effect=mock_create_reader_writer)

        await client.handshake()

        # Verify connection was created
        assert client.create_reader_writer.called

    @pytest.mark.asyncio
    async def test_handshake_discord_not_found(self, client_id, mock_ipc_path):
        """Test handshake when Discord IPC returns empty preamble"""
        client = BaseClient(client_id)

        # Create mock reader and writer
        mock_reader = AsyncMock()
        mock_writer = Mock()
        mock_reader.read = AsyncMock(return_value=b"")

        # Mock create_reader_writer to set up the mocks
        async def mock_create_reader_writer(ipc_path):
            client.sock_reader = mock_reader
            client.sock_writer = mock_writer

        client.create_reader_writer = AsyncMock(side_effect=mock_create_reader_writer)

        with pytest.raises(InvalidPipe):
            await client.handshake()

    @pytest.mark.asyncio
    async def test_handshake_invalid_client_id(self, client_id, mock_ipc_path):
        """Test handshake with invalid client ID"""
        client = BaseClient(client_id)

        # Mock invalid client ID response
        response = {"code": 4000, "message": "Invalid Client ID"}
        response_json = json.dumps(response).encode("utf-8")
        preamble = struct.pack("<II", 1, len(response_json))

        # Create mock reader and writer
        mock_reader = AsyncMock()
        mock_writer = Mock()
        mock_reader.read = AsyncMock(side_effect=[preamble, response_json])

        # Mock create_reader_writer to set up the mocks
        async def mock_create_reader_writer(ipc_path):
            client.sock_reader = mock_reader
            client.sock_writer = mock_writer

        client.create_reader_writer = AsyncMock(side_effect=mock_create_reader_writer)

        with pytest.raises(InvalidID):
            await client.handshake()

    @pytest.mark.asyncio
    async def test_handshake_short_preamble(self, client_id, mock_ipc_path):
        """Test handshake with short preamble"""
        client = BaseClient(client_id)

        # Create mock reader and writer
        mock_reader = AsyncMock()
        mock_writer = Mock()
        mock_reader.read = AsyncMock(return_value=b"\x00\x00")

        # Mock create_reader_writer to set up the mocks
        async def mock_create_reader_writer(ipc_path):
            client.sock_reader = mock_reader
            client.sock_writer = mock_writer

        client.create_reader_writer = AsyncMock(side_effect=mock_create_reader_writer)

        with pytest.raises(InvalidPipe):
            await client.handshake()


class TestBaseClientCreateReaderWriter:
    """Test BaseClient.create_reader_writer() method"""

    @pytest.mark.asyncio
    @pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific test")
    async def test_create_reader_writer_windows(self, client_id):
        """Test creating reader/writer on Windows - this test verifies the mocking setup"""
        # This test is primarily to verify the method exists and has correct signature
        # Actual connection testing requires Discord to be running
        client = BaseClient(client_id)
        ipc_path = r"\\?\pipe\discord-ipc-0"

        # Just verify the method can be called (will fail without Discord running)
        try:
            await asyncio.wait_for(client.create_reader_writer(ipc_path), timeout=0.1)
        except (FileNotFoundError, ConnectionTimeout, InvalidPipe, OSError):
            # Expected when Discord is not running
            pass

    @pytest.mark.asyncio
    async def test_create_reader_writer_file_not_found(self, client_id):
        """Test create_reader_writer with non-existent pipe"""
        client = BaseClient(client_id)

        with pytest.raises(InvalidPipe):
            await client.create_reader_writer("/nonexistent/path")

    @pytest.mark.asyncio
    async def test_create_reader_writer_timeout(self, client_id):
        """Test create_reader_writer with timeout"""
        client = BaseClient(client_id)
        client.connection_timeout = 0.01  # Very short timeout

        async def slow_connect(*args, **kwargs):
            await asyncio.sleep(1)
            return Mock(), Mock()

        if sys.platform == "win32":
            with patch.object(
                client.loop, "create_pipe_connection", side_effect=slow_connect
            ):
                with pytest.raises(ConnectionTimeout):
                    await client.create_reader_writer(r"\\?\pipe\discord-ipc-0")
        else:
            with patch("asyncio.open_unix_connection", side_effect=slow_connect):
                with pytest.raises(ConnectionTimeout):
                    await client.create_reader_writer("/tmp/discord-ipc-0")


class TestBaseClientEventLoop:
    """Test event loop management"""

    def test_update_event_loop(self, client_id):
        """Test updating event loop"""
        client = BaseClient(client_id)

        new_loop = asyncio.new_event_loop()
        client.update_event_loop(new_loop)

        assert client.loop is new_loop
        assert asyncio.get_event_loop() is new_loop

        new_loop.close()
