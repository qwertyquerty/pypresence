import enum


class ActivityType(enum.Enum):
    """
    https://discord.com/developers/docs/game-sdk/activities#data-models-activitytype-enum
    "type" must be one of 0, 2, 3, 5 -- Discord only implemented these four
    """

    PLAYING = 0
    # STREAMING = 1
    LISTENING = 2
    WATCHING = 3
    # CUSTOM = 4
    COMPETING = 5


class StatusDisplayType(enum.Enum):
    """
    https://discord.com/developers/docs/events/gateway-events#activity-object-status-display-types
    "status" must be one of 0, 1, 2 -- Discord only implemented these three
    """

    NAME = 0
    STATE = 1
    DETAILS = 2
