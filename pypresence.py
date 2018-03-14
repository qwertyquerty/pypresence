import asyncio
import json
import os
import struct
import sys
import time


class client:
    def __init__(self, client_id):
        if sys.platform == 'linux':
            self.ipc_path = (
                os.environ.get(
                    'XDG_RUNTIME_DIR',
                    None) or os.environ.get(
                    'TMPDIR',
                    None) or os.environ.get(
                    'TMP',
                    None) or os.environ.get(
                    'TEMP',
                    None) or '/tmp') + '/discord-ipc-0'
            self.loop = asyncio.get_event_loop()
        elif sys.platform == 'win32':
            self.ipc_path = r'\\?\pipe\discord-ipc-0'
            self.loop = asyncio.ProactorEventLoop()
        self.sock_reader: asyncio.StreamReader = None
        self.sock_writer: asyncio.StreamWriter = None
        self.client_id = client_id

    async def read_output(self):
        data = await self.sock_reader.read(1024)
        code, length = struct.unpack('<ii', data[:8])
        return json.loads(data[8:].decode('utf-8'))

    def send_data(self, op: int, payload: dict):
        payload = json.dumps(payload)
        print(payload)
        self.sock_writer.write(
            struct.pack(
                '<ii',
                op,
                len(payload)) +
            payload.encode('utf-8'))

    async def handshake(self):
        if sys.platform == 'linux':
            self.sock_reader, self.sock_writer = await asyncio.open_unix_connection(self.ipc_path, loop=self.loop)
        elif sys.platform == 'win32':
            self.sock_reader = asyncio.StreamReader(loop=self.loop)
            reader_protocol = asyncio.StreamReaderProtocol(
                self.sock_reader, loop=self.loop)
            self.sock_writer, _ = await self.loop.create_pipe_connection(lambda: reader_protocol, self.ipc_path)
        self.send_data(0, {'v': 1, 'client_id': self.client_id})
        data = await self.sock_reader.read(1024)
        code, length = struct.unpack('<ii', data[:8])

    def authorize(self, client_id, scopes):
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

    def set_user_voice_settings(self,user_id,pan_left=None,pan_right=None,volume=None,mute=None):
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

        if pan_left is None:
            del payload["args"]["pan"]["left"]
        if pan_right is None:
            del payload["args"]["pan"]["right"]
        if volume is None:
            del payload["args"]["volume"]
        if mute is None:
            del payload["args"]["mute"]

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

    def set_activity(self,pid=os.getpid(),state=None,details=None,start=None,end=None,large_image=None,large_text=None,small_image=None,small_text=None,party_id=None,party_size=None,join=None,spectate=None,match=None,instance=True):
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
        if state is None:
            del payload["args"]["activity"]["state"]
        if details is None:
            del payload["args"]["activity"]["details"]
        if start is None:
            del payload["args"]["activity"]["timestamps"]["start"]
        if end is None:
            del payload["args"]["activity"]["timestamps"]["end"]
        if large_image is None:
            del payload["args"]["activity"]["assets"]["large_image"]
        if large_text is None:
            del payload["args"]["activity"]["assets"]["large_text"]
        if small_image is None:
            del payload["args"]["activity"]["assets"]["small_image"]
        if small_text is None:
            del payload["args"]["activity"]["assets"]["small_text"]
        if party_id is None:
            del payload["args"]["activity"]["party"]["id"]
        if party_size is None:
            del payload["args"]["activity"]["party"]["size"]
        if join is None:
            del payload["args"]["activity"]["secrets"]["join"]
        if spectate is None:
            del payload["args"]["activity"]["secrets"]["spectate"]
        if match is None:
            del payload["args"]["activity"]["secrets"]["match"]
        if instance is None:
            del payload["args"]["activity"]["instance"]

        sent = self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def subscribe(self,event,args={}):
        current_time = time.time()
        payload = {
            "cmd": "SUBSCRIBE",
            "args": args,
            "evt": event,
            "nonce": '{:.20f}'.format(current_time)
        }
        sent = self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def unsubscribe(self,event,args={}):
        current_time = time.time()
        payload = {
            "cmd": "UNSUBSCRIBE",
            "args": args,
            "evt": event,
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
        sent = self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

        if _input is None:
            del payload["args"]["input"]
        if output is None:
            del payload["args"]["output"]
        if mode is None:
            del payload["args"]["mode"]
        if automatic_gain_control is None:
            del payload["args"]["automatic_gain_control"]
        if echo_cancellation is None:
            del payload["args"]["echo_cancellation"]
        if noise_suppression is None:
            del payload["args"]["noise_suppression"]
        if qos is None:
            del payload["args"]["qos"]
        if silence_warning is None:
            del payload["args"]["silence_warning"]
        if deaf is None:
            del payload["args"]["deaf"]
        if mute is None:
            del payload["args"]["mute"]

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

    def close(self):
        self.sock_writer.close()
        self.loop.close()

    def start(self):
        self.loop.run_until_complete(self.handshake())
