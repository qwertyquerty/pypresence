import enum


class ActivityType(enum.IntEnum):
    """
    Activity type enum for Discord Rich Presence.

    Specifies what type of activity is being displayed. Discord only supports types 0, 2, 3, and 5.
    Types 1 (STREAMING) and 4 (CUSTOM) are not available via Rich Presence.

    See: https://discord.com/developers/docs/game-sdk/activities#data-models-activitytype-enum

    Attributes
    ----------
    PLAYING : int
        Value 0. Shows "Playing {game name}" (default)
    LISTENING : int
        Value 2. Shows "Listening to {name}"
    WATCHING : int
        Value 3. Shows "Watching {name}"
    COMPETING : int
        Value 5. Shows "Competing in {name}"
    """

    PLAYING = 0
    # STREAMING = 1
    LISTENING = 2
    WATCHING = 3
    # CUSTOM = 4
    COMPETING = 5


class StatusDisplayType(enum.IntEnum):
    """
    Status display type enum for Discord Rich Presence.

    Controls which field from your presence is displayed in the user's Discord status bar.
    Discord only supports types 0, 1, and 2.

    See: https://discord.com/developers/docs/events/gateway-events#activity-object-status-display-types

    Attributes
    ----------
    NAME : int
        Value 0. Displays the application name (default)
    STATE : int
        Value 1. Displays the state field
    DETAILS : int
        Value 2. Displays the details field
    """

    NAME = 0
    STATE = 1
    DETAILS = 2
