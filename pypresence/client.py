from __future__ import annotations

import asyncio
import inspect
import json
import os
import struct
from typing import Any, Callable, List

from .baseclient import BaseClient
from .exceptions import (
    ArgumentError,
    DiscordError,
    EventNotFound,
    InvalidArgument,
    PyPresenceException,
)
from .payloads import Payload
from .types import ActivityType, StatusDisplayType


class Client(BaseClient):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._closed = False
        self._events: dict[str, Callable] = {}

    def register_event(
        self, event: str, func: Callable, args: dict | None = None
    ) -> None:
        if args is None:
            args = {}
        if inspect.iscoroutinefunction(func):
            raise NotImplementedError
        elif len(inspect.signature(func).parameters) != 1:
            raise ArgumentError
        self.subscribe(event, args)
        self._events[event.lower()] = func

    def unregister_event(self, event: str, args: dict | None = None) -> None:
        if args is None:
            args = {}
        event = event.lower()
        if event not in self._events:
            raise EventNotFound(event)
        self.unsubscribe(event, args)
        del self._events[event]

    # noinspection PyProtectedMember
    def on_event(self, data: bytes) -> None:
        assert self.sock_reader is not None
        # Reaching into StreamReader internals isn't in its public/typed
        # interface, hence the Any escape hatch.
        reader: Any = self.sock_reader
        if reader._eof:
            raise PyPresenceException("feed_data after feed_eof")
        if not data:
            return
        reader._buffer.extend(data)
        reader._wakeup_waiter()
        if (
            reader._transport is not None
            and not reader._paused
            and len(reader._buffer) > 2 * reader._limit
        ):
            try:
                reader._transport.pause_reading()
            except NotImplementedError:
                reader._transport = None
            else:
                reader._paused = True

        end = 0
        while end < len(data):
            # While chunks are available in data
            start = end + 8
            status_code, length = struct.unpack("<II", data[end:start])
            end = length + start
            payload = json.loads(data[start:end].decode("utf-8"))

            if payload["evt"] is not None:
                evt = payload["evt"].lower()
                if evt in self._events:
                    self._events[evt](payload["data"])
                elif evt == "error":
                    raise DiscordError(
                        payload["data"]["code"], payload["data"]["message"]
                    )

    def authorize(self, client_id: str, scopes: List[str]) -> dict:
        payload = Payload.authorize(client_id, scopes)
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def authenticate(self, token: str) -> dict:
        payload = Payload.authenticate(token)
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def get_guilds(self) -> dict:
        payload = Payload.get_guilds()
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def get_guild(self, guild_id: str) -> dict:
        payload = Payload.get_guild(guild_id)
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def get_channel(self, channel_id: str) -> dict:
        payload = Payload.get_channel(channel_id)
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def get_channels(self, guild_id: str) -> dict:
        payload = Payload.get_channels(guild_id)
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def set_user_voice_settings(
        self,
        user_id: str,
        pan_left: float | None = None,
        pan_right: float | None = None,
        volume: int | None = None,
        mute: bool | None = None,
    ) -> dict:
        payload = Payload.set_user_voice_settings(
            user_id, pan_left, pan_right, volume, mute
        )
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def select_voice_channel(self, channel_id: str) -> dict:
        payload = Payload.select_voice_channel(channel_id)
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def get_selected_voice_channel(self) -> dict:
        payload = Payload.get_selected_voice_channel()
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def select_text_channel(self, channel_id: str) -> dict:
        payload = Payload.select_text_channel(channel_id)
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def set_activity(
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
    ) -> dict:
        payload: Payload | dict
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

    def clear_activity(self, pid: int = os.getpid()) -> dict:
        payload = Payload.set_activity(pid, activity=None)
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def subscribe(self, event: str, args: dict | None = None) -> dict:
        if args is None:
            args = {}
        payload = Payload.subscribe(event, args)
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def unsubscribe(self, event: str, args: dict | None = None) -> dict:
        if args is None:
            args = {}
        payload = Payload.unsubscribe(event, args)
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def get_voice_settings(self) -> dict:
        payload = Payload.get_voice_settings()
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def set_voice_settings(
        self,
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
    ) -> dict:
        payload = Payload.set_voice_settings(
            _input,
            output,
            mode,
            automatic_gain_control,
            echo_cancellation,
            noise_suppression,
            qos,
            silence_warning,
            deaf,
            mute,
        )
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def capture_shortcut(self, action: str) -> dict:
        payload = Payload.capture_shortcut(action)
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def send_activity_join_invite(self, user_id: str) -> dict:
        payload = Payload.send_activity_join_invite(user_id)
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def close_activity_request(self, user_id: str) -> dict:
        payload = Payload.close_activity_request(user_id)
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def close(self) -> None:
        self.send_data(2, {"v": 1, "client_id": self.client_id})
        assert self.sock_writer is not None
        self.sock_writer.close()
        self._closed = True
        self.loop.close()

    def start(self) -> None:
        self.loop.run_until_complete(self.handshake())

    def read(self) -> dict:
        return self.loop.run_until_complete(self.read_output())


class AioClient(BaseClient):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs, isasync=True)
        self._closed = False
        self._events: dict[str, Callable] = {}

    async def register_event(
        self, event: str, func: Callable, args: dict | None = None
    ) -> None:
        if args is None:
            args = {}
        if not inspect.iscoroutinefunction(func):
            raise InvalidArgument(
                "Coroutine", "Subroutine", "Event function must be a coroutine"
            )
        elif len(inspect.signature(func).parameters) != 1:
            raise ArgumentError
        await self.subscribe(event, args)
        self._events[event.lower()] = func

    async def unregister_event(self, event: str, args: dict | None = None) -> None:
        if args is None:
            args = {}
        event = event.lower()
        if event not in self._events:
            raise EventNotFound(event)
        await self.unsubscribe(event, args)
        del self._events[event]

    # noinspection PyProtectedMember
    def on_event(self, data: bytes) -> None:
        assert self.sock_reader is not None
        # Reaching into StreamReader internals isn't in its public/typed
        # interface, hence the Any escape hatch.
        reader: Any = self.sock_reader
        if reader._eof:
            raise PyPresenceException("feed_data after feed_eof")
        if not data:
            return
        reader._buffer.extend(data)
        reader._wakeup_waiter()
        if (
            reader._transport is not None
            and not reader._paused
            and len(reader._buffer) > 2 * reader._limit
        ):
            try:
                reader._transport.pause_reading()
            except NotImplementedError:
                reader._transport = None
            else:
                reader._paused = True

        payload = json.loads(data[8:].decode("utf-8"))

        if payload["evt"] is not None:
            evt = payload["evt"].lower()
            if evt in self._events:
                asyncio.create_task(self._events[evt](payload["data"]))
            elif evt == "error":
                raise DiscordError(payload["data"]["code"], payload["data"]["message"])

    async def authorize(self, client_id: str, scopes: List[str]) -> dict:
        payload = Payload.authorize(client_id, scopes)
        self.send_data(1, payload)
        return await self.read_output()

    async def authenticate(self, token: str) -> dict:
        payload = Payload.authenticate(token)
        self.send_data(1, payload)
        return await self.read_output()

    async def get_guilds(self) -> dict:
        payload = Payload.get_guilds()
        self.send_data(1, payload)
        return await self.read_output()

    async def get_guild(self, guild_id: str) -> dict:
        payload = Payload.get_guild(guild_id)
        self.send_data(1, payload)
        return await self.read_output()

    async def get_channel(self, channel_id: str) -> dict:
        payload = Payload.get_channel(channel_id)
        self.send_data(1, payload)
        return await self.read_output()

    async def get_channels(self, guild_id: str) -> dict:
        payload = Payload.get_channels(guild_id)
        self.send_data(1, payload)
        return await self.read_output()

    async def set_user_voice_settings(
        self,
        user_id: str,
        pan_left: float | None = None,
        pan_right: float | None = None,
        volume: int | None = None,
        mute: bool | None = None,
    ) -> dict:
        payload = Payload.set_user_voice_settings(
            user_id, pan_left, pan_right, volume, mute
        )
        self.send_data(1, payload)
        return await self.read_output()

    async def select_voice_channel(self, channel_id: str) -> dict:
        payload = Payload.select_voice_channel(channel_id)
        self.send_data(1, payload)
        return await self.read_output()

    async def get_selected_voice_channel(self) -> dict:
        payload = Payload.get_selected_voice_channel()
        self.send_data(1, payload)
        return await self.read_output()

    async def select_text_channel(self, channel_id: str) -> dict:
        payload = Payload.select_text_channel(channel_id)
        self.send_data(1, payload)
        return await self.read_output()

    async def set_activity(
        self,
        pid: int = os.getpid(),
        activity_type: ActivityType | None = None,
        status_display_type: StatusDisplayType | None = None,
        state: str | None = None,
        details: str | None = None,
        name: str | None = None,
        start: int | None = None,
        end: int | None = None,
        large_image: str | None = None,
        large_text: str | None = None,
        small_image: str | None = None,
        small_text: str | None = None,
        party_id: str | None = None,
        party_size: list | None = None,
        join: str | None = None,
        spectate: str | None = None,
        match: str | None = None,
        buttons: list | None = None,
        instance: bool = True,
    ) -> dict:
        payload = Payload.set_activity(
            pid=pid,
            activity_type=activity_type.value if activity_type else None,
            status_display_type=(
                status_display_type.value if status_display_type else None
            ),
            state=state,
            details=details,
            name=name,
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
            activity=True,
        )
        self.send_data(1, payload)
        return await self.read_output()

    async def clear_activity(self, pid: int = os.getpid()) -> dict:
        payload = Payload.set_activity(pid, activity=None)
        self.send_data(1, payload)
        return await self.read_output()

    async def subscribe(self, event: str, args: dict | None = None) -> dict:
        if args is None:
            args = {}
        payload = Payload.subscribe(event, args)
        self.send_data(1, payload)
        return await self.read_output()

    async def unsubscribe(self, event: str, args: dict | None = None) -> dict:
        if args is None:
            args = {}
        payload = Payload.unsubscribe(event, args)
        self.send_data(1, payload)
        return await self.read_output()

    async def get_voice_settings(self) -> dict:
        payload = Payload.get_voice_settings()
        self.send_data(1, payload)
        return await self.read_output()

    async def set_voice_settings(
        self,
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
    ) -> dict:
        payload = Payload.set_voice_settings(
            _input,
            output,
            mode,
            automatic_gain_control,
            echo_cancellation,
            noise_suppression,
            qos,
            silence_warning,
            deaf,
            mute,
        )
        self.send_data(1, payload)
        return await self.read_output()

    async def capture_shortcut(self, action: str) -> dict:
        payload = Payload.capture_shortcut(action)
        self.send_data(1, payload)
        return await self.read_output()

    async def send_activity_join_invite(self, user_id: str) -> dict:
        payload = Payload.send_activity_join_invite(user_id)
        self.send_data(1, payload)
        return await self.read_output()

    async def close_activity_request(self, user_id: str) -> dict:
        payload = Payload.close_activity_request(user_id)
        self.send_data(1, payload)
        return await self.read_output()

    def close(self) -> None:
        self.send_data(2, {"v": 1, "client_id": self.client_id})
        assert self.sock_writer is not None
        self.sock_writer.close()
        self._closed = True
        self.loop.close()

    async def start(self) -> None:
        await self.handshake()

    async def read(self) -> dict:
        return await self.read_output()
