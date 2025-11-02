from __future__ import annotations

import os
import sys

from .baseclient import BaseClient
from .payloads import Payload
from .types import ActivityType, StatusDisplayType
from .utils import get_event_loop


class Presence(BaseClient):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update(
        self,
        pid: int = os.getpid(),
        activity_type: ActivityType | None = None,
        status_display_type: StatusDisplayType | None = None,
        state: str | None = None,
        state_url: str | None = None,
        details: str | None = None,
        details_url: str | None = None,
        name: str | None = None,
        start: int | None = None,
        end: int | None = None,
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
        payload_override: dict | None = None,
    ):
        if payload_override is None:
            payload = Payload.set_activity(
                pid=pid,
                activity_type=activity_type.value if activity_type else None,
                status_display_type=(
                    status_display_type.value if status_display_type else None
                ),
                state=state,
                state_url=state_url,
                details=details,
                details_url=details_url,
                name=name,
                start=start,
                end=end,
                large_image=large_image,
                large_text=large_text,
                large_url=large_url,
                small_image=small_image,
                small_text=small_text,
                small_url=small_url,
                party_id=party_id,
                party_size=party_size,
                join=join,
                spectate=spectate,
                match=match,
                buttons=buttons,
                instance=instance,
                activity=True,
            )
        else:
            payload = payload_override
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
        self.send_data(2, {"v": 1, "client_id": self.client_id})
        self.loop.close()
        if sys.platform == "win32":
            self.sock_writer._call_connection_lost(None)


class AioPresence(BaseClient):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, isasync=True)

    async def update(
        self,
        pid: int = os.getpid(),
        activity_type: ActivityType | None = None,
        status_display_type: StatusDisplayType | None = None,
        state: str | None = None,
        state_url: str | None = None,
        details: str | None = None,
        details_url: str | None = None,
        name: str | None = None,
        start: int | None = None,
        end: int | None = None,
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
    ):
        payload = Payload.set_activity(
            pid=pid,
            activity_type=activity_type,
            status_display_type=status_display_type,
            state=state,
            state_url=state_url,
            details=details,
            details_url=details_url,
            name=name,
            start=start,
            end=end,
            large_image=large_image,
            large_text=large_text,
            large_url=large_url,
            small_image=small_image,
            small_text=small_text,
            small_url=small_url,
            party_id=party_id,
            party_size=party_size,
            join=join,
            spectate=spectate,
            match=match,
            buttons=buttons,
            instance=instance,
            activity=True,
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
        self.send_data(2, {"v": 1, "client_id": self.client_id})
        self.loop.close()
        if sys.platform == "win32":
            self.sock_writer._call_connection_lost(None)
