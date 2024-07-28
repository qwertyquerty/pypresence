import enum

# https://discord.com/developers/docs/game-sdk/activities#data-models-activitytype-enum
# ""type" must be one of 0, 2, 3, 5" -- Discord only implemented these four
class ActivityType(enum.Enum):
    PLAYING = 0
    #STREAMING = 1
    LISTENING = 2
    WATCHING = 3
    #CUSTOM = 4
    COMPETING = 5
