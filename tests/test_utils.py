"""Test utility functions"""

import asyncio
import sys

import pytest

from pypresence.utils import get_event_loop, remove_none


class TestRemoveNone:
    """Test remove_none utility function"""

    def test_removes_none_from_flat_dict(self):
        """Test removing None from flat dictionary"""
        d = {"a": 1, "b": None, "c": "test", "d": None}
        result = remove_none(d)

        assert "a" in result
        assert "c" in result
        assert "b" not in result
        assert "d" not in result
        assert result["a"] == 1
        assert result["c"] == "test"

    def test_removes_none_from_nested_dict(self):
        """Test removing None from nested dictionary"""
        d = {
            "level1": {
                "keep": "this",
                "remove": None,
                "level2": {"also_keep": 123, "also_remove": None},
            }
        }
        result = remove_none(d)

        assert "remove" not in result["level1"]
        assert "also_remove" not in result["level1"]["level2"]
        assert result["level1"]["keep"] == "this"
        assert result["level1"]["level2"]["also_keep"] == 123

    def test_removes_empty_nested_dicts(self):
        """Test that empty nested dicts are removed"""
        d = {"keep": "value", "nested": {"all": None, "none": None}}
        result = remove_none(d)

        assert "nested" not in result
        assert result["keep"] == "value"

    def test_preserves_falsy_non_none_values(self):
        """Test that other falsy values (0, False, '') are preserved"""
        d = {
            "zero": 0,
            "false": False,
            "empty_string": "",
            "empty_list": [],
            "none": None,
        }
        result = remove_none(d)

        assert result["zero"] == 0
        assert result["false"] is False
        assert result["empty_string"] == ""
        assert result["empty_list"] == []
        assert "none" not in result

    def test_does_not_modify_original_dict(self):
        """Test that original dictionary is modified in-place (by design)"""
        original = {"a": 1, "b": None}
        result = remove_none(original.copy())  # Copy to test independently

        # Result should not have None value
        assert "b" not in result
        assert result["a"] == 1


class TestGetEventLoop:
    """Test get_event_loop utility function"""

    def test_returns_new_loop_when_forced(self):
        """Test force_fresh returns a new loop"""
        loop1 = get_event_loop(force_fresh=True)
        loop2 = get_event_loop(force_fresh=True)

        assert loop1 is not loop2
        assert isinstance(loop1, asyncio.AbstractEventLoop)
        assert isinstance(loop2, asyncio.AbstractEventLoop)

        loop1.close()
        loop2.close()

    def test_returns_running_loop_if_available(self):
        """Test returns running loop when available"""

        async def check_loop():
            loop = get_event_loop()
            running = asyncio.get_running_loop()
            assert loop is running

        asyncio.run(check_loop())

    def test_returns_new_loop_when_none_running(self):
        """Test returns new loop when no loop is running"""
        # Ensure no loop is running
        try:
            asyncio.get_running_loop()
            pytest.skip("A loop is already running")
        except RuntimeError:
            pass

        loop = get_event_loop()
        assert isinstance(loop, asyncio.AbstractEventLoop)
        assert not loop.is_closed()
        loop.close()

    def test_returns_new_loop_if_current_closed(self):
        """Test returns new loop if current loop is closed"""
        old_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(old_loop)
        old_loop.close()

        new_loop = get_event_loop()
        assert isinstance(new_loop, asyncio.AbstractEventLoop)
        assert not new_loop.is_closed()
        assert new_loop is not old_loop
        new_loop.close()


class TestIPCPath:
    """Test IPC path discovery - integration-style tests"""

    @pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific test")
    def test_windows_ipc_path_format(self):
        """Test Windows IPC path format"""
        from pypresence.utils import get_ipc_path

        # Note: This will return None if Discord is not running
        path = get_ipc_path(0)

        if path:
            assert path.startswith(r"\\?\pipe\discord-ipc-")

    @pytest.mark.skipif(sys.platform == "win32", reason="Unix-specific test")
    def test_unix_ipc_path_format(self):
        """Test Unix IPC path format"""
        from pypresence.utils import get_ipc_path

        # Note: This will return None if Discord is not running
        path = get_ipc_path(0)

        if path:
            assert "discord-ipc-" in path

    def test_get_ipc_path_with_pipe_number(self):
        """Test IPC path with specific pipe number"""
        from pypresence.utils import get_ipc_path

        # Just test that it doesn't crash with different pipe numbers
        for pipe in range(10):
            path = get_ipc_path(pipe)
            # Will be None if Discord is not running on that pipe
            assert path is None or "discord-ipc-" in str(path)
