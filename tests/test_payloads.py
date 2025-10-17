"""Test payload generation without any I/O operations"""

import json
import os

from pypresence.payloads import Payload
from pypresence.types import ActivityType, StatusDisplayType


class TestPayloadGeneration:
    """Test Payload class methods"""

    def test_basic_payload_creation(self):
        """Test creating a basic payload"""
        data = {"cmd": "TEST", "args": {"value": 1}}
        payload = Payload(data, clear_none=False)

        assert payload.data == data
        assert isinstance(str(payload), str)
        assert "TEST" in str(payload)

    def test_payload_removes_none_values(self):
        """Test that None values are removed by default"""
        data = {
            "cmd": "TEST",
            "args": {
                "value": 1,
                "none_value": None,
                "nested": {"keep": "this", "remove": None},
            },
        }
        payload = Payload(data, clear_none=True)

        assert "none_value" not in payload.data["args"]
        assert "remove" not in payload.data["args"]["nested"]
        assert payload.data["args"]["value"] == 1
        assert payload.data["args"]["nested"]["keep"] == "this"

    def test_payload_str_is_valid_json(self):
        """Test that __str__ returns valid JSON"""
        data = {"cmd": "TEST", "value": 123}
        payload = Payload(data)

        # Should be able to parse the string representation as JSON
        parsed = json.loads(str(payload))
        assert parsed["cmd"] == "TEST"
        assert parsed["value"] == 123


class TestSetActivity:
    """Test SET_ACTIVITY payload generation"""

    def test_set_activity_basic(self):
        """Test basic activity payload"""
        payload = Payload.set_activity(state="Testing", details="Running tests")

        assert payload.data["cmd"] == "SET_ACTIVITY"
        assert payload.data["args"]["activity"]["state"] == "Testing"
        assert payload.data["args"]["activity"]["details"] == "Running tests"
        assert "nonce" in payload.data

    def test_set_activity_with_timestamps(self):
        """Test activity with start/end timestamps"""
        start_time = 1234567890
        end_time = 1234567900

        payload = Payload.set_activity(start=start_time, end=end_time)

        assert payload.data["args"]["activity"]["timestamps"]["start"] == start_time
        assert payload.data["args"]["activity"]["timestamps"]["end"] == end_time

    def test_set_activity_with_images(self):
        """Test activity with large and small images"""
        payload = Payload.set_activity(
            large_image="large_key",
            large_text="Large Image Text",
            small_image="small_key",
            small_text="Small Image Text",
        )

        assets = payload.data["args"]["activity"]["assets"]
        assert assets["large_image"] == "large_key"
        assert assets["large_text"] == "Large Image Text"
        assert assets["small_image"] == "small_key"
        assert assets["small_text"] == "Small Image Text"

    def test_set_activity_with_party(self):
        """Test activity with party information"""
        payload = Payload.set_activity(party_id="party123", party_size=[1, 5])

        party = payload.data["args"]["activity"]["party"]
        assert party["id"] == "party123"
        assert party["size"] == [1, 5]

    def test_set_activity_with_buttons(self):
        """Test activity with buttons"""
        buttons = [
            {"label": "Button 1", "url": "https://example.com/1"},
            {"label": "Button 2", "url": "https://example.com/2"},
        ]

        payload = Payload.set_activity(buttons=buttons)

        assert payload.data["args"]["activity"]["buttons"] == buttons

    def test_set_activity_with_secrets(self):
        """Test activity with join/spectate secrets"""
        payload = Payload.set_activity(
            join="join_secret", spectate="spectate_secret", match="match_secret"
        )

        secrets = payload.data["args"]["activity"]["secrets"]
        assert secrets["join"] == "join_secret"
        assert secrets["spectate"] == "spectate_secret"
        assert secrets["match"] == "match_secret"

    def test_set_activity_with_activity_type(self):
        """Test activity with different activity types"""
        for activity_type in ActivityType:
            payload = Payload.set_activity(activity_type=activity_type)
            assert payload.data["args"]["activity"]["type"] == activity_type.value

    def test_set_activity_with_activity_type_int(self):
        """Test activity type can be specified as int"""
        payload = Payload.set_activity(activity_type=2)  # LISTENING
        assert payload.data["args"]["activity"]["type"] == 2

    def test_set_activity_with_status_display_type(self):
        """Test activity with different status display types"""
        for status_type in StatusDisplayType:
            payload = Payload.set_activity(status_display_type=status_type)
            assert (
                payload.data["args"]["activity"]["status_display_type"]
                == status_type.value
            )

    def test_set_activity_with_name(self):
        """Test activity with name parameter"""
        payload = Payload.set_activity(name="Custom Activity Name")

        assert payload.data["args"]["activity"]["name"] == "Custom Activity Name"

    def test_set_activity_with_name_and_details(self):
        """Test activity with both name and details"""
        payload = Payload.set_activity(
            name="My Activity", details="Doing something", state="In progress"
        )

        assert payload.data["args"]["activity"]["name"] == "My Activity"
        assert payload.data["args"]["activity"]["details"] == "Doing something"
        assert payload.data["args"]["activity"]["state"] == "In progress"

    def test_set_activity_name_with_status_display_type(self):
        """Test activity with name and status display type set to NAME"""
        payload = Payload.set_activity(
            name="Custom Name", status_display_type=StatusDisplayType.NAME
        )

        assert payload.data["args"]["activity"]["name"] == "Custom Name"
        assert (
            payload.data["args"]["activity"]["status_display_type"]
            == StatusDisplayType.NAME.value
        )

    def test_set_activity_name_none_is_removed(self):
        """Test that name=None is removed from payload"""
        payload = Payload.set_activity(name=None, state="Testing")

        # None values should be removed by clear_none
        assert "name" not in payload.data["args"]["activity"]
        assert payload.data["args"]["activity"]["state"] == "Testing"

    def test_set_activity_clear(self):
        """Test clearing activity (activity=None)"""
        # When activity=None, clear is set to True and removes the activity field
        payload = Payload.set_activity(activity=None)

        assert payload.data["cmd"] == "SET_ACTIVITY"
        # The payload creation clears None values, so check that cmd exists
        assert "cmd" in payload.data

    def test_set_activity_with_pid(self):
        """Test activity with custom PID"""
        custom_pid = 12345
        payload = Payload.set_activity(pid=custom_pid)

        assert payload.data["args"]["pid"] == custom_pid

    def test_set_activity_default_pid(self):
        """Test activity uses current process PID by default"""
        payload = Payload.set_activity()

        assert payload.data["args"]["pid"] == os.getpid()

    def test_set_activity_instance_flag(self):
        """Test activity instance flag"""
        payload = Payload.set_activity(instance=False)
        assert payload.data["args"]["activity"]["instance"] is False

        payload = Payload.set_activity(instance=True)
        assert payload.data["args"]["activity"]["instance"] is True

    def test_set_activity_removes_empty_nested_dicts(self):
        """Test that empty nested dictionaries are removed"""
        payload = Payload.set_activity(state="Test")

        # These should be removed if empty
        activity = payload.data["args"]["activity"]

        # Timestamps should be removed if both are None
        assert "timestamps" not in activity or activity["timestamps"]

        # Assets should be removed if all are None
        assert "assets" not in activity or activity["assets"]

    def test_nonce_is_unique(self):
        """Test that each payload gets a unique nonce"""
        import time

        payload1 = Payload.set_activity(state="Test 1")
        time.sleep(0.001)  # Small delay to ensure different timestamp
        payload2 = Payload.set_activity(state="Test 2")

        assert payload1.data["nonce"] != payload2.data["nonce"]


class TestSetActivityURLFeatures:
    """Test SET_ACTIVITY payload generation with URL parameters"""

    def test_set_activity_with_state_url(self):
        """Test activity with state URL"""
        payload = Payload.set_activity(
            state="Playing a game", state_url="https://example.com/game"
        )

        assert payload.data["args"]["activity"]["state"] == "Playing a game"
        assert (
            payload.data["args"]["activity"]["state_url"] == "https://example.com/game"
        )

    def test_set_activity_with_details_url(self):
        """Test activity with details URL"""
        payload = Payload.set_activity(
            details="In a match", details_url="https://example.com/match/123"
        )

        assert payload.data["args"]["activity"]["details"] == "In a match"
        assert (
            payload.data["args"]["activity"]["details_url"]
            == "https://example.com/match/123"
        )

    def test_set_activity_with_large_url(self):
        """Test activity with large image URL"""
        payload = Payload.set_activity(
            large_image="large_key",
            large_text="Large Image",
            large_url="https://example.com/images/large.png",
        )

        assets = payload.data["args"]["activity"]["assets"]
        assert assets["large_image"] == "large_key"
        assert assets["large_text"] == "Large Image"
        assert assets["large_url"] == "https://example.com/images/large.png"

    def test_set_activity_with_small_url(self):
        """Test activity with small image URL"""
        payload = Payload.set_activity(
            small_image="small_key",
            small_text="Small Image",
            small_url="https://example.com/images/small.png",
        )

        assets = payload.data["args"]["activity"]["assets"]
        assert assets["small_image"] == "small_key"
        assert assets["small_text"] == "Small Image"
        assert assets["small_url"] == "https://example.com/images/small.png"

    def test_set_activity_with_all_urls(self):
        """Test activity with all URL parameters"""
        payload = Payload.set_activity(
            state="Playing",
            state_url="https://example.com/state",
            details="Match in progress",
            details_url="https://example.com/details",
            large_image="large",
            large_url="https://example.com/large.png",
            small_image="small",
            small_url="https://example.com/small.png",
        )

        activity = payload.data["args"]["activity"]
        assert activity["state_url"] == "https://example.com/state"
        assert activity["details_url"] == "https://example.com/details"

        assets = activity["assets"]
        assert assets["large_url"] == "https://example.com/large.png"
        assert assets["small_url"] == "https://example.com/small.png"

    def test_set_activity_url_without_corresponding_field(self):
        """Test that URL can be set even without the corresponding text field"""
        payload = Payload.set_activity(state_url="https://example.com/state")

        # URL should still be present even if state is None
        activity = payload.data["args"]["activity"]
        assert activity["state_url"] == "https://example.com/state"

    def test_set_activity_image_url_without_image_key(self):
        """Test that image URL can be set without the image key"""
        payload = Payload.set_activity(large_url="https://example.com/large.png")

        assets = payload.data["args"]["activity"]["assets"]
        assert assets["large_url"] == "https://example.com/large.png"

    def test_set_activity_urls_none_are_removed(self):
        """Test that URL fields with None values are removed"""
        payload = Payload.set_activity(
            state="Testing", state_url=None, details="Details", details_url=None
        )

        activity = payload.data["args"]["activity"]
        assert "state_url" not in activity
        assert "details_url" not in activity
        assert activity["state"] == "Testing"
        assert activity["details"] == "Details"

    def test_set_activity_mixed_urls_and_regular_fields(self):
        """Test activity with mix of URLs and regular fields"""
        payload = Payload.set_activity(
            state="Current State",
            state_url="https://example.com/state",
            details="Current Details",
            large_image="large_key",
            large_text="Large Image Text",
            large_url="https://cdn.example.com/large.png",
            buttons=[{"label": "Website", "url": "https://example.com"}],
        )

        activity = payload.data["args"]["activity"]
        assert activity["state"] == "Current State"
        assert activity["state_url"] == "https://example.com/state"
        assert activity["details"] == "Current Details"

        assets = activity["assets"]
        assert assets["large_image"] == "large_key"
        assert assets["large_text"] == "Large Image Text"
        assert assets["large_url"] == "https://cdn.example.com/large.png"

        assert activity["buttons"] == [
            {"label": "Website", "url": "https://example.com"}
        ]
