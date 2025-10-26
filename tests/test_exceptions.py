"""Test exception classes"""

import pytest

from pypresence.exceptions import (
    ConnectionTimeout,
    DiscordError,
    DiscordNotFound,
    InvalidArgument,
    InvalidID,
    InvalidPipe,
    PipeClosed,
    PyPresenceException,
    ResponseTimeout,
    ServerError,
)


class TestExceptions:
    """Test exception classes"""

    def test_pypresence_exception_is_base(self):
        """Test that PyPresenceException is the base exception"""
        assert issubclass(InvalidArgument, PyPresenceException)
        assert issubclass(InvalidPipe, PyPresenceException)
        assert issubclass(DiscordNotFound, PyPresenceException)

    def test_invalid_argument_exception(self):
        """Test InvalidArgument exception"""
        exc = InvalidArgument("expected", "received", "Extra message")

        assert "expected" in str(exc)
        assert "received" in str(exc)
        assert "Extra message" in str(exc)

    def test_discord_error_exception(self):
        """Test DiscordError exception"""
        exc = DiscordError(4000, "Invalid Client ID")

        assert exc.code == 4000
        assert "4000" in str(exc)
        assert "Invalid Client ID" in str(exc)

    def test_server_error_exception(self):
        """Test ServerError exception"""
        exc = ServerError("Server error message")

        assert "Server error message" in str(exc)

    def test_exceptions_can_be_raised_and_caught(self):
        """Test that exceptions can be raised and caught"""
        with pytest.raises(PipeClosed):
            raise PipeClosed()

        with pytest.raises(ConnectionTimeout):
            raise ConnectionTimeout()

        with pytest.raises(ResponseTimeout):
            raise ResponseTimeout()

        with pytest.raises(DiscordNotFound):
            raise DiscordNotFound()

        with pytest.raises(InvalidID):
            raise InvalidID()

        with pytest.raises(InvalidPipe):
            raise InvalidPipe()

    def test_exceptions_inherit_from_base(self):
        """Test that all exceptions can be caught as PyPresenceException"""
        exceptions = [
            InvalidArgument("a", "b"),
            InvalidPipe(),
            PipeClosed(),
            ConnectionTimeout(),
            ResponseTimeout(),
            DiscordNotFound(),
            InvalidID(),
            DiscordError(4000, "test"),
            ServerError("test"),
        ]

        for exc in exceptions:
            assert isinstance(exc, PyPresenceException)
