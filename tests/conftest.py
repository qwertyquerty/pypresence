"""Pytest configuration and shared fixtures"""

import asyncio
import json
import struct
from unittest.mock import AsyncMock, MagicMock, Mock

import pytest


@pytest.fixture
def mock_event_loop():
    """Provide a fresh event loop for tests"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture
def mock_stream_reader():
    """Mock asyncio StreamReader"""
    reader = AsyncMock(spec=asyncio.StreamReader)
    return reader


@pytest.fixture
def mock_stream_writer():
    """Mock asyncio StreamWriter"""
    writer = MagicMock(spec=asyncio.StreamWriter)
    writer.write = Mock()
    writer._call_connection_lost = Mock()
    return writer


@pytest.fixture
def mock_ipc_connection(mock_stream_reader, mock_stream_writer):
    """Mock a successful IPC connection with handshake response"""
    # Mock successful handshake response
    handshake_response = {
        "cmd": "DISPATCH",
        "data": {
            "v": 1,
            "config": {
                "cdn_host": "cdn.discordapp.com",
                "api_endpoint": "//discord.com/api",
                "environment": "production",
            },
        },
        "evt": "READY",
        "nonce": None,
    }

    response_json = json.dumps(handshake_response).encode("utf-8")
    preamble = struct.pack("<II", 1, len(response_json))

    mock_stream_reader.read = AsyncMock(
        side_effect=[
            preamble,  # First read for handshake
            response_json,  # Second read for handshake data
        ]
    )

    return mock_stream_reader, mock_stream_writer


@pytest.fixture
def mock_discord_response():
    """Factory fixture for creating mock Discord responses"""

    def _create_response(evt="ACTIVITY_UPDATE", data=None, error=False):
        if error:
            response = {"evt": "ERROR", "data": {"message": data or "Test error"}}
        else:
            response = {
                "cmd": "SET_ACTIVITY",
                "data": data or {},
                "evt": evt,
                "nonce": "test_nonce",
            }

        response_json = json.dumps(response).encode("utf-8")
        preamble = struct.pack("<II", 1, len(response_json))
        return preamble + response_json

    return _create_response


@pytest.fixture
def client_id():
    """Test client ID"""
    return "1234567890123456789"


@pytest.fixture
def mock_ipc_path(monkeypatch, tmp_path):
    """Mock IPC path discovery"""
    import sys

    if sys.platform == "win32":
        ipc_path = r"\\?\pipe\discord-ipc-0"
    else:
        ipc_path = str(tmp_path / "discord-ipc-0")

    def mock_get_ipc_path(pipe=None):
        return ipc_path

    # Patch in baseclient module where it's actually used
    from pypresence import baseclient

    monkeypatch.setattr(baseclient, "get_ipc_path", mock_get_ipc_path)

    return ipc_path
