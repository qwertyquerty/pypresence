import inspect
import json
import os
import time

from .baseclient import BaseClient
from .exceptions import *
from .utils import *


class Client(BaseClient):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self._closed = False
        self._events = {}

    def register_event(self, event: str, func, args={}):
        if inspect.iscoroutinefunction(func):
            raise NotImplementedError
        elif len(inspect.signature(func).parameters) != 1:
            raise ArgumentError
        self.subscribe(event, args)
        self._events[event.lower()] = func

    def unregister_event(self, event: str, args={}):
        event = event.lower()
        if event not in self._events:
            raise EventNotFound
        self.unsubscribe(event, args)
        del self._events[event]

    def on_event(self, data):
        if self.sock_reader._eof:
            raise PyPresenceException('feed_data after feed_eof')
        if not data:
            return
        self.sock_reader._buffer.extend(data)
        self.sock_reader._wakeup_waiter()
        if (self.sock_reader._transport is not None and
                not self.sock_reader._paused and
                len(self.sock_reader._buffer) > 2 * self.sock_reader._limit):
            try:
                self.sock_reader._transport.pause_reading()
            except NotImplementedError:
                self.sock_reader._transport = None
            else:
                self.sock_reader._paused = True

        payload = json.loads(data[8:].decode('utf-8'))

        if payload["evt"] is not None:
            evt = payload["evt"].lower()
            if evt in self._events:
                self._events[evt](payload["data"])
            elif evt == 'error':
                raise DiscordError(payload["data"]["code"], payload["data"]["message"])

    def authorize(self, client_id,scopes):
        current_time = time.time()
        payload = {
            "cmd": "AUTHORIZE",
            "args": {
                "client_id": str(client_id),
                "scopes": scopes
            },
            "nonce": '{:.20f}'.format(current_time)
        }
        sent = self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def authenticate(self, token):
        current_time = time.time()
        payload = {
            "cmd": "AUTHENTICATE",
            "args": {
                "access_token": token
            },
            "nonce": '{:.20f}'.format(current_time)
        }

        sent = self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def get_guilds(self):
        current_time = time.time()
        payload = {
            "cmd": "GET_GUILDS",
            "args": {
            },
            "nonce": '{:.20f}'.format(current_time)
        }
        sent = self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def get_guild(self, guild_id):
        current_time = time.time()
        payload = {
            "cmd": "GET_GUILD",
            "args": {
                "guild_id": str(guild_id),
            },
            "nonce": '{:.20f}'.format(current_time)
        }
        sent = self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def get_channel(self, channel_id):
        current_time = time.time()
        payload = {
            "cmd": "GET_CHANNEL",
            "args": {
                "channel_id": str(channel_id),
            },
            "nonce": '{:.20f}'.format(current_time)
        }
        sent = self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def get_channels(self, guild_id):
        current_time = time.time()
        payload = {
            "cmd": "GET_CHANNELS",
            "args": {
                "guild_id": str(guild_id),
            },
            "nonce": '{:.20f}'.format(current_time)
        }
        sent = self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def set_user_voice_settings(self, user_id, pan_left=None, pan_right=None, volume=None, mute=None):
        current_time = time.time()
        payload = {
            "cmd": "SET_USER_VOICE_SETTINGS",
            "args": {
                "user_id": str(user_id),
                "pan": {
                    "left": pan_left,
                    "right": pan_right
                },
                "volume": volume,
                "mute": mute
            },
            "nonce": '{:.20f}'.format(current_time)
        }

        payload = remove_none(payload)

        sent = self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def select_voice_channel(self, channel_id):
        current_time = time.time()
        payload = {
            "cmd": "SELECT_VOICE_CHANNEL",
            "args": {
                "channel_id": str(channel_id),
            },
            "nonce": '{:.20f}'.format(current_time)
        }
        sent = self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def get_selected_voice_channel(self):
        current_time = time.time()
        payload = {
            "cmd": "GET_SELECTED_VOICE_CHANNEL",
            "args": {
            },
            "nonce": '{:.20f}'.format(current_time)
        }
        sent = self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def select_text_channel(self, channel_id):
        current_time = time.time()
        payload = {
            "cmd": "SELECT_VOICE_CHANNEL",
            "args": {
                "channel_id": str(channel_id),
            },
            "nonce": '{:.20f}'.format(current_time)
        }
        sent = self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def set_activity(self, pid=os.getpid(), state=None, details=None, start=None, end=None, large_image=None, large_text=None, small_image=None, small_text=None, party_id=None, party_size=None, join=None, spectate=None, match=None, instance=True):
        current_time = time.time()
        payload = {
            "cmd": "SET_ACTIVITY",
            "args": {
                "pid": pid,
                "activity": {
                    "state": state,
                    "details": details,
                    "timestamps": {
                        "start": start,
                        "end": end
                    },
                    "assets": {
                        "large_image": large_image,
                        "large_text": large_text,
                        "small_image": small_image,
                        "small_text": small_text
                    },
                    "party": {
                        "id": party_id,
                        "size": party_size
                    },
                    "secrets": {
                        "join": join,
                        "spectate": spectate,
                        "match": match
                    },
                    "instance": instance,
                },
            },
            "nonce": '{:.20f}'.format(current_time)
        }
        payload = remove_none(payload)

        sent = self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def clear_activity(self, pid=os.getpid()):
        current_time = time.time()
        payload = {
            "cmd": "SET_ACTIVITY",
            "args": {
                "pid": pid,
                "activity": None
            },
            "nonce": '{:.20f}'.format(current_time)
        }
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def subscribe(self, event, args={}):
        current_time = time.time()
        payload = {
            "cmd": "SUBSCRIBE",
            "args": args,
            "evt": event.upper(),
            "nonce": '{:.20f}'.format(current_time)
        }
        sent = self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def unsubscribe(self, event, args={}):
        current_time = time.time()
        payload = {
            "cmd": "UNSUBSCRIBE",
            "args": args,
            "evt": event.upper(),
            "nonce": '{:.20f}'.format(current_time)
        }
        sent = self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def get_voice_settings(self):
        current_time = time.time()
        payload = {
            "cmd": "GET_VOICE_SETTINGS",
            "args": {},
            "nonce": '{:.20f}'.format(current_time)
        }
        sent = self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def set_voice_settings(self,_input=None,output=None,mode=None,automatic_gain_control=None,echo_cancellation=None,noise_suppression=None,qos=None,silence_warning=None,deaf=None,mute=None):
        current_time = time.time()
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
                "mute": mute
            },
            "nonce": '{:.20f}'.format(current_time)
        }
        payload = remove_none(payload)
        sent = self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def capture_shortcut(self, action):
        current_time = time.time()
        payload = {
            "cmd": "CAPTURE_SHORTCUT",
            "args": {
                "action": action.upper()
            },
            "nonce": '{:.20f}'.format(current_time)
        }
        sent = self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def send_activity_join_invite(self, user_id):
        current_time = time.time()
        payload = {
            "cmd": "SEND_ACTIVITY_JOIN_INVITE",
            "args": {
                "user_id": str(user_id)
            },
            "nonce": '{:.20f}'.format(current_time)
        }
        sent = self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def close_activity_request(self, user_id):
        current_time = time.time()
        payload = {
            "cmd": "CLOSE_ACTIVITY_REQUEST",
            "args": {
                "user_id": str(user_id)
            },
            "nonce": '{:.20f}'.format(current_time)
        }
        sent = self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def close(self):
        self.send_data(2, {'v': 1, 'client_id': self.client_id})
        self.sock_writer.close()
        self._closed = True
        self.loop.close()

    def start(self):
        self.loop.run_until_complete(self.handshake())

    def read(self):
        return self.loop.run_until_complete(self.read_output())
