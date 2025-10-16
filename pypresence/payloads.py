from __future__ import annotations

import json
import os
import time

from .utils import remove_none
from .types import ActivityType, StatusDisplayType


class Payload:

    def __init__(self, data, clear_none=True):
        if clear_none:
            data = remove_none(data)
        self.data = data

    def __str__(self):
        return json.dumps(self.data, indent=2)

    @staticmethod
    def time():
        return time.time()

    @classmethod
    def set_activity(
        cls,
        pid: int = os.getpid(),
        activity_type: ActivityType | int | None = None,
        status_display_type: StatusDisplayType | int | None = None,
        state: str | None = None,
        state_url: str | None = None,
        details: str | None = None,
        details_url: str | None = None,
        start: int | float | None = None,
        end: int | float | None = None,
        large_image: str | None = None,
        large_text: str | None = None,
        large_url: str | None = None,
        small_image: str | None = None,
        small_text: str | None = None,
        small_url: str | None = None,
        party_id: str | None = None,
        party_size: list | None = None,
        join: str | None = None,
        spectate: str | None = None,
        match: str | None = None,
        buttons: list | None = None,
        instance: bool = True,
        activity: bool | None = True,
        _rn: bool = True,
    ):

        # They should already be an int because we give typehints, but some people are fucking stupid and use
        # IDLE or some other stupid shit.
        if start:
            start = int(start)
        if end:
            end = int(end)

        if isinstance(activity_type, int):
            activity_type = ActivityType(activity_type)
        if isinstance(status_display_type, int):
            status_display_type = StatusDisplayType(status_display_type)

        if activity is None:
            act_details = None
            clear = True
        else:
            act_details = {
                "type": (
                    activity_type.value
                    if isinstance(activity_type, ActivityType)
                    else ActivityType.PLAYING
                ),
                "status_display_type": (
                    status_display_type
                    if isinstance(status_display_type, StatusDisplayType)
                    else StatusDisplayType.NAME
                ),
                "state": state,
                "state_url": state_url,
                "details": details,
                "details_url": details_url,
                "timestamps": {"start": start, "end": end},
                "assets": {
                    "large_image": large_image,
                    "large_text": large_text,
                    "large_url": large_url,
                    "small_image": small_image,
                    "small_text": small_text,
                    "small_url": small_url,
                },
                "party": {"id": party_id, "size": party_size},
                "secrets": {"join": join, "spectate": spectate, "match": match},
                "buttons": buttons,
                "instance": instance,
            }
            clear = False

        payload = {
            "cmd": "SET_ACTIVITY",
            "args": {"pid": pid, "activity": act_details},
            "nonce": "{:.20f}".format(cls.time()),
        }
        if _rn:
            clear = _rn
        return cls(payload, clear)

    @classmethod
    def authorize(cls, client_id: str, scopes: list[str]):
        payload = {
            "cmd": "AUTHORIZE",
            "args": {"client_id": str(client_id), "scopes": scopes},
            "nonce": "{:.20f}".format(cls.time()),
        }
        return cls(payload)

    @classmethod
    def authenticate(cls, token: str):
        payload = {
            "cmd": "AUTHENTICATE",
            "args": {"access_token": token},
            "nonce": "{:.20f}".format(cls.time()),
        }

        return cls(payload)

    @classmethod
    def get_guilds(cls):
        payload = {
            "cmd": "GET_GUILDS",
            "args": {},
            "nonce": "{:.20f}".format(cls.time()),
        }

        return cls(payload)

    @classmethod
    def get_guild(cls, guild_id: str):
        payload = {
            "cmd": "GET_GUILD",
            "args": {
                "guild_id": str(guild_id),
            },
            "nonce": "{:.20f}".format(cls.time()),
        }

        return cls(payload)

    @classmethod
    def get_channels(cls, guild_id: str):
        payload = {
            "cmd": "GET_CHANNELS",
            "args": {
                "guild_id": str(guild_id),
            },
            "nonce": "{:.20f}".format(cls.time()),
        }

        return cls(payload)

    @classmethod
    def get_channel(cls, channel_id: str):
        payload = {
            "cmd": "GET_CHANNEL",
            "args": {
                "channel_id": str(channel_id),
            },
            "nonce": "{:.20f}".format(cls.time()),
        }

        return cls(payload)

    @classmethod
    def set_user_voice_settings(
        cls,
        user_id: str,
        pan_left: float | None = None,
        pan_right: float | None = None,
        volume: int | None = None,
        mute: bool | None = None,
    ):
        payload = {
            "cmd": "SET_USER_VOICE_SETTINGS",
            "args": {
                "user_id": str(user_id),
                "pan": {"left": pan_left, "right": pan_right},
                "volume": volume,
                "mute": mute,
            },
            "nonce": "{:.20f}".format(cls.time()),
        }

        return cls(payload, True)

    @classmethod
    def select_voice_channel(cls, channel_id: str):
        payload = {
            "cmd": "SELECT_VOICE_CHANNEL",
            "args": {
                "channel_id": str(channel_id),
            },
            "nonce": "{:.20f}".format(cls.time()),
        }

        return cls(payload)

    @classmethod
    def get_selected_voice_channel(cls):
        payload = {
            "cmd": "GET_SELECTED_VOICE_CHANNEL",
            "args": {},
            "nonce": "{:.20f}".format(cls.time()),
        }

        return cls(payload)

    @classmethod
    def select_text_channel(cls, channel_id: str):
        payload = {
            "cmd": "SELECT_TEXT_CHANNEL",
            "args": {
                "channel_id": str(channel_id),
            },
            "nonce": "{:.20f}".format(cls.time()),
        }

        return cls(payload)

    @classmethod
    def subscribe(cls, event: str, args=None):
        if args is None:
            args = {}
        payload = {
            "cmd": "SUBSCRIBE",
            "args": args,
            "evt": event.upper(),
            "nonce": "{:.20f}".format(cls.time()),
        }

        return cls(payload)

    @classmethod
    def unsubscribe(cls, event: str, args=None):
        if args is None:
            args = {}
        payload = {
            "cmd": "UNSUBSCRIBE",
            "args": args,
            "evt": event.upper(),
            "nonce": "{:.20f}".format(cls.time()),
        }

        return cls(payload)

    @classmethod
    def get_voice_settings(cls):
        payload = {
            "cmd": "GET_VOICE_SETTINGS",
            "args": {},
            "nonce": "{:.20f}".format(cls.time()),
        }

        return cls(payload)

    @classmethod
    def set_voice_settings(
        cls,
        _input: dict | None = None,
        output: dict | None = None,
        mode: dict | None = None,
        automatic_gain_control: bool | None = None,
        echo_cancellation: bool | None = None,
        noise_suppression: bool | None = None,
        qos: bool | None = None,
        silence_warning: bool | None = None,
        deaf: bool | None = None,
        mute: bool | None = None,
    ):
        payload = {
            "cmd": "SET_VOICE_SETTINGS",
            "args": {
                "input": _input,
                "output": output,
                "mode": mode,
                "automatic_gain_control": automatic_gain_control,
                "echo_cancellation": echo_cancellation,
                "noise_suppression": noise_suppression,
                "qos": qos,
                "silence_warning": silence_warning,
                "deaf": deaf,
                "mute": mute,
            },
            "nonce": "{:.20f}".format(cls.time()),
        }

        return cls(payload, True)

    @classmethod
    def capture_shortcut(cls, action: str):
        payload = {
            "cmd": "CAPTURE_SHORTCUT",
            "args": {"action": action.upper()},
            "nonce": "{:.20f}".format(cls.time()),
        }

        return cls(payload)

    @classmethod
    def send_activity_join_invite(cls, user_id: str):
        payload = {
            "cmd": "SEND_ACTIVITY_JOIN_INVITE",
            "args": {"user_id": str(user_id)},
            "nonce": "{:.20f}".format(cls.time()),
        }

        return cls(payload)

    @classmethod
    def close_activity_request(cls, user_id: str):
        payload = {
            "cmd": "CLOSE_ACTIVITY_REQUEST",
            "args": {"user_id": str(user_id)},
            "nonce": "{:.20f}".format(cls.time()),
        }

        return cls(payload)
