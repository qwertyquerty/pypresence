"""Test Presence class with mocked I/O"""

import json
import struct
from unittest.mock import AsyncMock, Mock, patch

import pytest

from pypresence import AioPresence, Presence
from pypresence.types import ActivityType


class TestPresenceInit:
    """Test Presence initialization"""

    def test_presence_init_basic(self, client_id):
        """Test basic Presence initialization"""
        presence = Presence(client_id)

        assert presence.client_id == client_id
        assert presence.isasync is False
        assert presence.connection_timeout == 30
        assert presence.response_timeout == 10

    def test_presence_init_with_custom_timeouts(self, client_id):
        """Test Presence with custom timeouts"""
        presence = Presence(client_id, connection_timeout=60, response_timeout=20)

        assert presence.connection_timeout == 60
        assert presence.response_timeout == 20

    def test_presence_init_with_pipe(self, client_id):
        """Test Presence with specific pipe"""
        presence = Presence(client_id, pipe=5)

        assert presence.pipe == 5


class TestPresenceUpdate:
    """Test Presence.update() method"""

    @patch("pypresence.baseclient.BaseClient.read_output")
    def test_update_basic(self, mock_read_output, client_id):
        """Test basic presence update"""
        presence = Presence(client_id)
        presence.sock_writer = Mock()

        # Mock read_output to return success
        mock_output = {"cmd": "SET_ACTIVITY", "evt": "ACTIVITY_UPDATE", "data": {}}
        mock_read_output.return_value = AsyncMock(return_value=mock_output)

        # Call update
        presence.update(state="Testing", details="Test Details")

        # Verify send_data was called with correct opcode
        assert presence.sock_writer.write.called

        # Verify the payload sent contains our state and details
        call_args = presence.sock_writer.write.call_args[0][0]
        op, length = struct.unpack("<II", call_args[:8])
        payload_json = call_args[8 : 8 + length].decode("utf-8")
        payload = json.loads(payload_json)

        assert payload["cmd"] == "SET_ACTIVITY"
        assert payload["args"]["activity"]["state"] == "Testing"
        assert payload["args"]["activity"]["details"] == "Test Details"

    @patch("pypresence.baseclient.BaseClient.read_output")
    def test_update_with_activity_type(self, mock_read_output, client_id):
        """Test update with activity type"""
        presence = Presence(client_id)
        presence.sock_writer = Mock()

        async def mock_coro():
            return {}

        mock_read_output.return_value = mock_coro()

        presence.update(activity_type=ActivityType.LISTENING)

        call_args = presence.sock_writer.write.call_args[0][0]
        op, length = struct.unpack("<II", call_args[:8])
        payload_json = call_args[8 : 8 + length].decode("utf-8")
        payload = json.loads(payload_json)

        assert payload["args"]["activity"]["type"] == ActivityType.LISTENING.value

    @patch("pypresence.baseclient.BaseClient.read_output")
    def test_update_with_name(self, mock_read_output, client_id):
        """Test update with name parameter"""
        presence = Presence(client_id)
        presence.sock_writer = Mock()

        async def mock_coro():
            return {}

        mock_read_output.return_value = mock_coro()

        presence.update(name="Custom Activity Name")

        call_args = presence.sock_writer.write.call_args[0][0]
        op, length = struct.unpack("<II", call_args[:8])
        payload_json = call_args[8 : 8 + length].decode("utf-8")
        payload = json.loads(payload_json)

        assert payload["args"]["activity"]["name"] == "Custom Activity Name"

    @patch("pypresence.baseclient.BaseClient.read_output")
    def test_update_with_name_and_status_display_type(
        self, mock_read_output, client_id
    ):
        """Test update with name and status_display_type"""
        presence = Presence(client_id)
        presence.sock_writer = Mock()

        async def mock_coro():
            return {}

        mock_read_output.return_value = mock_coro()

        from pypresence.types import StatusDisplayType

        presence.update(
            name="My Custom Name", status_display_type=StatusDisplayType.NAME
        )

        call_args = presence.sock_writer.write.call_args[0][0]
        op, length = struct.unpack("<II", call_args[:8])
        payload_json = call_args[8 : 8 + length].decode("utf-8")
        payload = json.loads(payload_json)

        assert payload["args"]["activity"]["name"] == "My Custom Name"
        assert (
            payload["args"]["activity"]["status_display_type"]
            == StatusDisplayType.NAME.value
        )

    @patch("pypresence.baseclient.BaseClient.read_output")
    def test_update_with_name_details_and_state(self, mock_read_output, client_id):
        """Test update with name, details, and state together"""
        presence = Presence(client_id)
        presence.sock_writer = Mock()

        async def mock_coro():
            return {}

        mock_read_output.return_value = mock_coro()

        presence.update(
            name="My Activity", details="Working on something", state="In Progress"
        )

        call_args = presence.sock_writer.write.call_args[0][0]
        op, length = struct.unpack("<II", call_args[:8])
        payload_json = call_args[8 : 8 + length].decode("utf-8")
        payload = json.loads(payload_json)

        assert payload["args"]["activity"]["name"] == "My Activity"
        assert payload["args"]["activity"]["details"] == "Working on something"
        assert payload["args"]["activity"]["state"] == "In Progress"


class TestPresenceClear:
    """Test Presence.clear() method"""

    @patch("pypresence.baseclient.BaseClient.read_output")
    def test_clear(self, mock_read_output, client_id):
        """Test clearing presence"""
        presence = Presence(client_id)
        presence.sock_writer = Mock()

        # Mock read_output properly
        mock_read_output.return_value = AsyncMock(return_value={})

        presence.clear()

        # Verify send_data was called
        assert presence.sock_writer.write.called

        # Check payload - the clear uses activity=None which gets removed by remove_none
        call_args = presence.sock_writer.write.call_args[0][0]
        op, length = struct.unpack("<II", call_args[:8])
        payload_json = call_args[8 : 8 + length].decode("utf-8")
        payload = json.loads(payload_json)

        # After clear_none, activity field won't be in the payload
        assert payload["cmd"] == "SET_ACTIVITY"


class TestPresenceConnect:
    """Test Presence.connect() method"""

    @patch("pypresence.baseclient.BaseClient.handshake")
    def test_connect(self, mock_handshake, client_id, mock_ipc_path):
        """Test connecting to Discord"""
        presence = Presence(client_id)

        # Mock the handshake to be a successful coroutine
        async def mock_coro():
            return None

        mock_handshake.return_value = mock_coro()

        presence.connect()

        # Verify handshake was called
        assert mock_handshake.called


class TestPresenceClose:
    """Test Presence.close() method"""

    def test_close(self, client_id):
        """Test closing presence connection"""
        import sys

        presence = Presence(client_id)
        presence.sock_writer = Mock()
        presence.sock_writer._call_connection_lost = Mock()

        presence.close()

        # Verify close payload was sent
        assert presence.sock_writer.write.called

        # Verify loop was closed
        assert presence.loop.is_closed()

        # On Windows, verify connection_lost was called
        if sys.platform == "win32":
            assert presence.sock_writer._call_connection_lost.called


class TestAioPresence:
    """Test async Presence class"""

    def test_aio_presence_init(self, client_id):
        """Test AioPresence initialization"""
        presence = AioPresence(client_id)

        assert presence.client_id == client_id
        assert presence.isasync is True

    @pytest.mark.asyncio
    async def test_aio_presence_update(self, client_id, mock_discord_response):
        """Test async presence update"""
        presence = AioPresence(client_id)
        presence.sock_writer = Mock()

        # Mock read_output
        mock_response = {"cmd": "SET_ACTIVITY", "evt": "ACTIVITY_UPDATE", "data": {}}
        presence.read_output = AsyncMock(return_value=mock_response)

        result = await presence.update(state="Testing")

        assert result == mock_response
        assert presence.sock_writer.write.called


class TestPresenceURLFeatures:
    """Test Presence URL features (state_url, details_url, large_url, small_url)"""

    @patch("pypresence.baseclient.BaseClient.read_output")
    def test_update_with_state_url(self, mock_read_output, client_id):
        """Test presence update with state_url parameter"""
        presence = Presence(client_id)
        presence.sock_writer = Mock()

        async def mock_coro():
            return {}

        mock_read_output.return_value = mock_coro()

        presence.update(state="Playing a game", state_url="https://example.com/game")

        # Parse the payload
        call_args = presence.sock_writer.write.call_args[0][0]
        op, length = struct.unpack("<II", call_args[:8])
        payload_json = call_args[8 : 8 + length].decode("utf-8")
        payload = json.loads(payload_json)

        assert payload["args"]["activity"]["state"] == "Playing a game"
        assert payload["args"]["activity"]["state_url"] == "https://example.com/game"

    @patch("pypresence.baseclient.BaseClient.read_output")
    def test_update_with_details_url(self, mock_read_output, client_id):
        """Test presence update with details_url parameter"""
        presence = Presence(client_id)
        presence.sock_writer = Mock()

        async def mock_coro():
            return {}

        mock_read_output.return_value = mock_coro()

        presence.update(
            details="In a ranked match", details_url="https://example.com/match/12345"
        )

        # Parse the payload
        call_args = presence.sock_writer.write.call_args[0][0]
        op, length = struct.unpack("<II", call_args[:8])
        payload_json = call_args[8 : 8 + length].decode("utf-8")
        payload = json.loads(payload_json)

        assert payload["args"]["activity"]["details"] == "In a ranked match"
        assert (
            payload["args"]["activity"]["details_url"]
            == "https://example.com/match/12345"
        )

    @patch("pypresence.baseclient.BaseClient.read_output")
    def test_update_with_large_url(self, mock_read_output, client_id):
        """Test presence update with large_url parameter"""
        presence = Presence(client_id)
        presence.sock_writer = Mock()

        async def mock_coro():
            return {}

        mock_read_output.return_value = mock_coro()

        presence.update(
            large_image="large_key",
            large_text="Large Image",
            large_url="https://cdn.example.com/images/large.png",
        )

        # Parse the payload
        call_args = presence.sock_writer.write.call_args[0][0]
        op, length = struct.unpack("<II", call_args[:8])
        payload_json = call_args[8 : 8 + length].decode("utf-8")
        payload = json.loads(payload_json)

        assets = payload["args"]["activity"]["assets"]
        assert assets["large_image"] == "large_key"
        assert assets["large_text"] == "Large Image"
        assert assets["large_url"] == "https://cdn.example.com/images/large.png"

    @patch("pypresence.baseclient.BaseClient.read_output")
    def test_update_with_small_url(self, mock_read_output, client_id):
        """Test presence update with small_url parameter"""
        presence = Presence(client_id)
        presence.sock_writer = Mock()

        async def mock_coro():
            return {}

        mock_read_output.return_value = mock_coro()

        presence.update(
            small_image="small_key",
            small_text="Small Image",
            small_url="https://cdn.example.com/images/small.png",
        )

        # Parse the payload
        call_args = presence.sock_writer.write.call_args[0][0]
        op, length = struct.unpack("<II", call_args[:8])
        payload_json = call_args[8 : 8 + length].decode("utf-8")
        payload = json.loads(payload_json)

        assets = payload["args"]["activity"]["assets"]
        assert assets["small_image"] == "small_key"
        assert assets["small_text"] == "Small Image"
        assert assets["small_url"] == "https://cdn.example.com/images/small.png"

    @patch("pypresence.baseclient.BaseClient.read_output")
    def test_update_with_all_urls(self, mock_read_output, client_id):
        """Test presence update with all URL parameters"""
        presence = Presence(client_id)
        presence.sock_writer = Mock()

        async def mock_coro():
            return {}

        mock_read_output.return_value = mock_coro()

        presence.update(
            state="Playing",
            state_url="https://example.com/state",
            details="Match in progress",
            details_url="https://example.com/details",
            large_image="large",
            large_url="https://cdn.example.com/large.png",
            small_image="small",
            small_url="https://cdn.example.com/small.png",
        )

        # Parse the payload
        call_args = presence.sock_writer.write.call_args[0][0]
        op, length = struct.unpack("<II", call_args[:8])
        payload_json = call_args[8 : 8 + length].decode("utf-8")
        payload = json.loads(payload_json)

        activity = payload["args"]["activity"]
        assert activity["state_url"] == "https://example.com/state"
        assert activity["details_url"] == "https://example.com/details"

        assets = activity["assets"]
        assert assets["large_url"] == "https://cdn.example.com/large.png"
        assert assets["small_url"] == "https://cdn.example.com/small.png"


class TestAioPresenceURLFeatures:
    """Test async Presence URL features"""

    @pytest.mark.asyncio
    async def test_aio_update_with_state_url(self, client_id):
        """Test async presence update with state_url"""
        presence = AioPresence(client_id)
        presence.sock_writer = Mock()

        mock_response = {"cmd": "SET_ACTIVITY", "evt": "ACTIVITY_UPDATE", "data": {}}
        presence.read_output = AsyncMock(return_value=mock_response)

        await presence.update(
            state="Playing async", state_url="https://example.com/async"
        )

        # Parse the payload
        call_args = presence.sock_writer.write.call_args[0][0]
        op, length = struct.unpack("<II", call_args[:8])
        payload_json = call_args[8 : 8 + length].decode("utf-8")
        payload = json.loads(payload_json)

        assert payload["args"]["activity"]["state"] == "Playing async"
        assert payload["args"]["activity"]["state_url"] == "https://example.com/async"

    @pytest.mark.asyncio
    async def test_aio_update_with_all_urls(self, client_id):
        """Test async presence update with all URL parameters"""
        presence = AioPresence(client_id)
        presence.sock_writer = Mock()

        mock_response = {"cmd": "SET_ACTIVITY", "evt": "ACTIVITY_UPDATE", "data": {}}
        presence.read_output = AsyncMock(return_value=mock_response)

        await presence.update(
            state="Async State",
            state_url="https://example.com/state",
            details="Async Details",
            details_url="https://example.com/details",
            large_image="large",
            large_url="https://cdn.example.com/large.png",
            small_image="small",
            small_url="https://cdn.example.com/small.png",
        )

        # Parse the payload
        call_args = presence.sock_writer.write.call_args[0][0]
        op, length = struct.unpack("<II", call_args[:8])
        payload_json = call_args[8 : 8 + length].decode("utf-8")
        payload = json.loads(payload_json)

        activity = payload["args"]["activity"]
        assert activity["state_url"] == "https://example.com/state"
        assert activity["details_url"] == "https://example.com/details"

        assets = activity["assets"]
        assert assets["large_url"] == "https://cdn.example.com/large.png"
        assert assets["small_url"] == "https://cdn.example.com/small.png"
