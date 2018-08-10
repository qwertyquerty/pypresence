import os
import time

from .utils import *
from .baseclient import BaseClient


class Presence(BaseClient):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

    def update(self,pid=os.getpid(),state=None,details=None,start=None,end=None,large_image=None,large_text=None,small_image=None,small_text=None,party_id=None,party_size=None,join=None,spectate=None,match=None,instance=True):
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

        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def clear(self,pid=os.getpid()):
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
