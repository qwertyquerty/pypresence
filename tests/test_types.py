"""Test type enums"""

from pypresence.types import ActivityType, StatusDisplayType


class TestActivityType:
    """Test ActivityType enum"""

    def test_activity_type_values(self):
        """Test ActivityType enum values"""
        assert ActivityType.PLAYING.value == 0
        # STREAMING not implemented in Discord
        assert ActivityType.LISTENING.value == 2
        assert ActivityType.WATCHING.value == 3
        assert ActivityType.COMPETING.value == 5

    def test_activity_type_from_value(self):
        """Test creating ActivityType from value"""
        assert ActivityType(0) == ActivityType.PLAYING
        # ActivityType(1) STREAMING not implemented in Discord
        assert ActivityType(2) == ActivityType.LISTENING
        assert ActivityType(3) == ActivityType.WATCHING
        assert ActivityType(5) == ActivityType.COMPETING

    def test_activity_type_names(self):
        """Test ActivityType names"""
        assert ActivityType.PLAYING.name == "PLAYING"
        # STREAMING not implemented in Discord
        assert ActivityType.LISTENING.name == "LISTENING"
        assert ActivityType.WATCHING.name == "WATCHING"
        assert ActivityType.COMPETING.name == "COMPETING"

    def test_activity_type_iteration(self):
        """Test iterating over ActivityType"""
        types = list(ActivityType)
        assert (
            len(types) == 4
        )  # Only 4 implemented: PLAYING, LISTENING, WATCHING, COMPETING
        assert ActivityType.PLAYING in types
        assert ActivityType.COMPETING in types


class TestStatusDisplayType:
    """Test StatusDisplayType enum"""

    def test_status_display_type_values(self):
        """Test StatusDisplayType enum values"""
        assert StatusDisplayType.NAME.value == 0
        assert StatusDisplayType.STATE.value == 1
        assert StatusDisplayType.DETAILS.value == 2

    def test_status_display_type_from_value(self):
        """Test creating StatusDisplayType from value"""
        assert StatusDisplayType(0) == StatusDisplayType.NAME
        assert StatusDisplayType(1) == StatusDisplayType.STATE
        assert StatusDisplayType(2) == StatusDisplayType.DETAILS

    def test_status_display_type_names(self):
        """Test StatusDisplayType names"""
        assert StatusDisplayType.NAME.name == "NAME"
        assert StatusDisplayType.STATE.name == "STATE"
        assert StatusDisplayType.DETAILS.name == "DETAILS"

    def test_status_display_type_iteration(self):
        """Test iterating over StatusDisplayType"""
        types = list(StatusDisplayType)
        assert len(types) == 3
        assert StatusDisplayType.NAME in types
        assert StatusDisplayType.DETAILS in types
