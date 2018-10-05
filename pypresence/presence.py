import json
import os
import time

from .baseclient import BaseClient
from .utils import remove_none, payload_gen


class Presence(BaseClient):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update(self, pid: int = os.getpid(),
               state: str = None, details: str = None,
               start: int = None, end: int = None,
               large_image: str = None, large_text: str = None,
               small_image: str = None, small_text: str = None,
               party_id: str = None, party_size: list = None,
               join: str = None, spectate: str = None,
               match: str = None, instance: bool = True):

        payload_dict = {
            "pid": pid,
            "state": state,
            "details": details,
            "start": start,
            "end": end,
            "large_image": large_image,
            "large_text": large_text,
            "small_image": small_image,
            "small_text": small_text,
            "party_id": party_id,
            "party_size": party_size,
            "join": join,
            "spectate": spectate,
            "match": match,
            "instance": instance,
        }
        payload = payload_gen('set_activity', payload_dict)
        payload = remove_none(payload)
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def clear(self, pid: int = os.getpid()):
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

    def connect(self):
        self.loop.run_until_complete(self.handshake())

    def close(self):
        self.send_data(2, {'v': 1, 'client_id': self.client_id})
        self.sock_writer.close()
        self.loop.close()


class AioPresence(BaseClient):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, async=True)

    async def update(self, pid: int = os.getpid(),
                     state: str = None, details: str = None,
                     start: int = None, end: int = None,
                     large_image: str = None, large_text: str = None,
                     small_image: str = None, small_text: str = None,
                     party_id: str = None, party_size: list = None,
                     join: str = None, spectate: str = None,
                     match: str = None, instance: bool = True):
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
                    "instance": instance
                }
            },
            "nonce": '{:.20f}'.format(current_time)
        }
        payload = remove_none(payload)
        self.send_data(1, payload)
        return await self.read_output()

    async def clear(self, pid: int = os.getpid()):
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
        return await self.read_output()

    def close(self):
        self.send_data(2, {'v': 1, 'client_id': self.client_id})
        self.sock_writer.close()
        self.loop.close()
