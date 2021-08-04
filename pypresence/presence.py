import os

from .baseclient import BaseClient
from .payloads import Payload
from .utils import get_event_loop


class Presence(BaseClient):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update(
        self,
        pid: int = os.getpid(),
        state: str = None,
        details: str = None,
        start: int = None,
        end: int = None,
        large_image: str = None,
        large_text: str = None,
        small_image: str = None,
        small_text: str = None,
        party_id: str = None,
        party_size: list = None,
        join: str = None,
        spectate: str = None,
        match: str = None,
        buttons: list = None,
        instance: bool = True,
        _do_not_use=True
    ):

        if _do_not_use is True:
            payload = Payload.set_activity(
                pid=pid,
                state=state,
                details=details,
                start=start,
                end=end,
                large_image=large_image,
                large_text=large_text,
                small_image=small_image,
                small_text=small_text,
                party_id=party_id,
                party_size=party_size,
                join=join,
                spectate=spectate,
                match=match,
                buttons=buttons,
                instance=instance,
            )

        else:
            payload = _do_not_use

        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def clear(self, pid: int = os.getpid()):
        payload = Payload.set_activity(pid, activity=None)
        self.send_data(1, payload)

        return self.loop.run_until_complete(self.read_output())

    def connect(self):
        self.update_event_loop(get_event_loop())
        self.loop.run_until_complete(self.handshake())

    def close(self):
        self.send_data(2, {'v': 1, 'client_id': self.client_id})
        self.sock_writer.close()
        self.loop.close()


class AioPresence(BaseClient):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, isasync=True)

    async def update(
        self, pid: int = os.getpid(),
        state: str = None,
        details: str = None,
        start: int = None,
        end: int = None,
        large_image: str = None,
        large_text: str = None,
        small_image: str = None,
        small_text: str = None,
        party_id: str = None,
        party_size: list = None,
        join: str = None,
        spectate: str = None,
        match: str = None,
        buttons: list = None,
        instance: bool = True
    ):
        payload = Payload.set_activity(
            pid=pid,
            state=state,
            details=details,
            start=start,
            end=end,
            large_image=large_image,
            large_text=large_text,
            small_image=small_image,
            small_text=small_text,
            party_id=party_id,
            party_size=party_size,
            join=join,
            spectate=spectate,
            match=match,
            buttons=buttons,
            instance=instance
        )

        self.send_data(1, payload)
        return await self.read_output()

    async def clear(self, pid: int = os.getpid()):
        payload = Payload.set_activity(pid, activity=None)
        self.send_data(1, payload)
        return await self.read_output()

    async def connect(self):
        self.update_event_loop(get_event_loop())
        await self.handshake()

    def close(self):
        self.send_data(2, {'v': 1, 'client_id': self.client_id})
        self.sock_writer.close()
        self.loop.close()
