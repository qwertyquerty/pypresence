from __future__ import annotations

import asyncio
import inspect
import json
import os
import struct
from typing import Callable, List

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
    """
    Discord RPC Client.

    Creates a full-featured RPC client with authorization, subscriptions, and event handling capabilities.
    Use this class when you need access to advanced Discord RPC features beyond simple Rich Presence.

    Parameters
    ----------
    client_id : str
        OAuth2 App ID (found at https://discord.com/developers/applications/me)
    pipe : int, optional
        Pipe that should be used to connect to the Discord client. Defaults to 0, can be 0-9
    loop : asyncio.BaseEventLoop, optional
        Your own event loop (if you have one) that PyPresence should use. One will be created if not supplied.
        Information at https://docs.python.org/3/library/asyncio-eventloop.html
    handler : function, optional
        The exception handler pypresence should send asynchronous errors to. This can be a coroutine or
        standard function as long as it takes two arguments (exception, future). Exception will be the
        exception to handle and future will be an instance of asyncio.Future

    Examples
    --------
    >>> from pypresence import Client
    >>> RPC = Client("client_id")
    >>> RPC.start()
    >>> RPC.set_activity(state="Playing a game", details="In the main menu")
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._closed = False
        self._events = {}

    def register_event(self, event: str, func: Callable, args=None):
        """
        Hook an event to a function.

        The function will be called whenever Discord sends that event. Will automatically subscribe to the event.

        Parameters
        ----------
        event : str
            The event to hook
        func : function
            The function to pair with the event. Must accept exactly one argument (the event data).
        args : dict, optional
            Optional args used in subscription

        Returns
        -------
        None

        Raises
        ------
        NotImplementedError
            If func is a coroutine function (use AioClient for async)
        ArgumentError
            If func does not accept exactly one parameter
        """
        if args is None:
            args = {}
        if inspect.iscoroutinefunction(func):
            raise NotImplementedError
        elif len(inspect.signature(func).parameters) != 1:
            raise ArgumentError
        self.subscribe(event, args)
        self._events[event.lower()] = func

    def unregister_event(self, event: str, args=None):
        """
        Unhook an event from a function.

        Will automatically unsubscribe from the event as well.

        Parameters
        ----------
        event : str
            The event to unhook
        args : dict, optional
            Optional args used in unsubscription

        Returns
        -------
        None

        Raises
        ------
        EventNotFound
            If the event is not currently registered
        """
        if args is None:
            args = {}
        event = event.lower()
        if event not in self._events:
            raise EventNotFound(event)
        self.unsubscribe(event, args)
        del self._events[event]

    # noinspection PyProtectedMember
    def on_event(self, data):
        if self.sock_reader._eof:
            raise PyPresenceException("feed_data after feed_eof")
        if not data:
            return
        self.sock_reader._buffer.extend(data)
        self.sock_reader._wakeup_waiter()
        if (
            self.sock_reader._transport is not None
            and not self.sock_reader._paused
            and len(self.sock_reader._buffer) > 2 * self.sock_reader._limit
        ):
            try:
                self.sock_reader._transport.pause_reading()
            except NotImplementedError:
                self.sock_reader._transport = None
            else:
                self.sock_reader._paused = True

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

    def authorize(self, client_id: str, scopes: List[str]):
        """
        Authenticate a new client with your app.

        By default this pops up a modal in-app that asks the user to authorize access to your app.

        Parameters
        ----------
        client_id : str
            OAuth2 application id
        scopes : list of str
            A list of OAuth scopes as strings.
            All scopes can be found at https://discord.com/developers/docs/topics/oauth2

        Returns
        -------
        Response
            The response from Discord
        """
        payload = Payload.authorize(client_id, scopes)
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def authenticate(self, token: str):
        """
        Authenticate an existing client with your app.

        Parameters
        ----------
        token : str
            OAuth2 access token

        Returns
        -------
        Response
            The response from Discord
        """
        payload = Payload.authenticate(token)
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def get_guilds(self):
        """
        Get a list of guilds the client is in.

        Returns
        -------
        Response
            The response from Discord containing guild information
        """
        payload = Payload.get_guilds()
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def get_guild(self, guild_id: str):
        """
        Get information about a specific guild.

        Parameters
        ----------
        guild_id : str
            ID of the guild to get

        Returns
        -------
        Response
            The response from Discord containing guild information
        """
        payload = Payload.get_guild(guild_id)
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def get_channel(self, channel_id: str):
        """
        Get a channel the client is in.

        Parameters
        ----------
        channel_id : str
            ID of the channel to get

        Returns
        -------
        Response
            The response from Discord containing channel information
        """
        payload = Payload.get_channel(channel_id)
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def get_channels(self, guild_id: str):
        """
        Get a guild's channels the client is in.

        Parameters
        ----------
        guild_id : str
            ID of the guild to get channels from

        Returns
        -------
        Response
            The response from Discord containing channel information
        """
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
    ):
        """
        Set voice settings for a specific user.

        Parameters
        ----------
        user_id : str
            User ID
        pan_left : float, optional
            Left pan of the user
        pan_right : float, optional
            Right pan of the user
        volume : int, optional
            The volume of user (defaults to 100, min 0, max 200)
        mute : bool, optional
            The mute state of the user

        Returns
        -------
        Response
            The response from Discord
        """
        payload = Payload.set_user_voice_settings(
            user_id, pan_left, pan_right, volume, mute
        )
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def select_voice_channel(self, channel_id: str):
        """
        Join or leave a voice channel, group DM, or DM.

        Parameters
        ----------
        channel_id : str
            Channel ID to join (or None to leave)

        Returns
        -------
        Response
            The response from Discord
        """
        payload = Payload.select_voice_channel(channel_id)
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def get_selected_voice_channel(self):
        """
        Get the client's current voice channel.

        Returns
        -------
        Response
            The response from Discord containing current voice channel information
        """
        payload = Payload.get_selected_voice_channel()
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def select_text_channel(self, channel_id: str):
        """
        Join or leave a text channel, group DM, or DM.

        Parameters
        ----------
        channel_id : str
            Channel ID to join (or None to leave)

        Returns
        -------
        Response
            The response from Discord
        """
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
    ):
        """
        Set the activity shown on Discord profiles and status of users.

        Parameters
        ----------
        pid : int, optional
            The process id of your game. Defaults to current process ID.
        activity_type : ActivityType, optional
            The type of activity (PLAYING, LISTENING, WATCHING, or COMPETING). See ActivityType enum.
            Defaults to PLAYING if not specified.
        status_display_type : StatusDisplayType, optional
            Which field to display in the status (NAME, STATE, or DETAILS). See StatusDisplayType enum.
            Defaults to NAME if not specified.
        state : str, optional
            The user's current status
        state_url : str, optional
            URL to make the state text clickable (opens when state is clicked)
        details : str, optional
            What the player is currently doing
        details_url : str, optional
            URL to make the details text clickable (opens when details is clicked)
        name : str, optional
            Directly set what Discord will display in places like the user list
        start : int, optional
            Epoch time for game start (in milliseconds)
        end : int, optional
            Epoch time for game end (in milliseconds)
        large_image : str, optional
            Name of the uploaded image for the large profile artwork
        large_text : str, optional
            Tooltip for the large image
        large_url : str, optional
            URL to make the large image clickable (opens when large image is clicked)
        small_image : str, optional
            Name of the uploaded image for the small profile artwork
        small_text : str, optional
            Tooltip for the small image
        small_url : str, optional
            URL to make the small image clickable (opens when small image is clicked)
        party_id : str, optional
            ID of the player's party, lobby, or group
        party_size : list, optional
            Current size of the player's party, lobby, or group, and the max in this format: [1, 4]
        join : str, optional
            Unique hashed string for chat invitations and ask to join
        spectate : str, optional
            Unique hashed string for spectate button
        match : str, optional
            Unique hashed string for spectate and join
        buttons : list, optional
            List of dicts for buttons on your profile in the format [{"label": "My Website", "url": "https://example.com"}, ...],
            can list up to two buttons
        instance : bool, optional
            Marks the match as a game session with a specific beginning and end. Defaults to True.
        payload_override : dict, optional
            Custom payload to send instead of generating one from the parameters

        Returns
        -------
        Response
            The response from Discord
        """
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

    def clear_activity(self, pid: int = os.getpid()):
        """
        Clear the activity.

        Parameters
        ----------
        pid : int, optional
            The process id of your game. Defaults to current process ID.

        Returns
        -------
        Response
            The response from Discord
        """
        payload = Payload.set_activity(pid, activity=None)
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def subscribe(self, event: str, args=None):
        """
        Subscribe to events.

        Parameters
        ----------
        event : str
            Event name to subscribe to
        args : dict, optional
            Any args to go along with the event

        Returns
        -------
        Response
            The response from Discord
        """
        if args is None:
            args = {}
        payload = Payload.subscribe(event, args)
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def unsubscribe(self, event: str, args=None):
        """
        Unsubscribe from events.

        Parameters
        ----------
        event : str
            Event name to unsubscribe from
        args : dict, optional
            Any args to go along with the event

        Returns
        -------
        Response
            The response from Discord
        """
        if args is None:
            args = {}
        payload = Payload.unsubscribe(event, args)
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def get_voice_settings(self):
        """
        Get the user's voice settings.

        Returns
        -------
        Response
            The response from Discord containing voice settings
        """
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
    ):
        """
        Set the user's voice settings.

        Parameters
        ----------
        _input : dict, optional
            Input settings
        output : dict, optional
            Output settings
        mode : dict, optional
            Voice mode settings
        automatic_gain_control : bool, optional
            State of automatic gain control
        echo_cancellation : bool, optional
            State of echo cancellation
        noise_suppression : bool, optional
            State of noise suppression
        qos : bool, optional
            State of voice quality of service
        silence_warning : bool, optional
            State of silence warning notice
        deaf : bool, optional
            State of self-deafen
        mute : bool, optional
            State of self-mute

        Returns
        -------
        Response
            The response from Discord
        """
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

    def capture_shortcut(self, action: str):
        """
        Capture a keyboard shortcut entered by the user.

        Parameters
        ----------
        action : str
            Capture action, either 'START' or 'STOP'

        Returns
        -------
        Response
            The response from Discord
        """
        payload = Payload.capture_shortcut(action)
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def send_activity_join_invite(self, user_id: str):
        """
        Accept an Ask to Join request.

        Parameters
        ----------
        user_id : str
            User ID

        Returns
        -------
        Response
            The response from Discord
        """
        payload = Payload.send_activity_join_invite(user_id)
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def close_activity_request(self, user_id: str):
        """
        Reject an Ask to Join request.

        Parameters
        ----------
        user_id : str
            User ID

        Returns
        -------
        Response
            The response from Discord
        """
        payload = Payload.close_activity_request(user_id)
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def close(self):
        """
        Close the connection to Discord.

        Returns
        -------
        None
        """
        self.send_data(2, {"v": 1, "client_id": self.client_id})
        self.sock_writer.close()
        self._closed = True
        self.loop.close()

    def start(self):
        """
        Initialize the connection to Discord.

        This must be called before making any RPC commands.

        Returns
        -------
        None
        """
        self.loop.run_until_complete(self.handshake())

    def read(self):
        """
        Read output from Discord.

        Returns
        -------
        Response
            The response from Discord
        """
        return self.loop.run_until_complete(self.read_output())


class AioClient(BaseClient):
    """
    Async Discord RPC Client.

    Creates an asynchronous full-featured RPC client with authorization, subscriptions, and event handling capabilities.
    This class should be used with async/await syntax.

    Parameters
    ----------
    client_id : str
        OAuth2 App ID (found at https://discord.com/developers/applications/me)
    pipe : int, optional
        Pipe that should be used to connect to the Discord client. Defaults to 0, can be 0-9
    loop : asyncio.BaseEventLoop, optional
        Your own event loop (if you have one) that PyPresence should use. One will be created if not supplied.
        Information at https://docs.python.org/3/library/asyncio-eventloop.html
    handler : function, optional
        The exception handler pypresence should send asynchronous errors to. This must be a coroutine
        that takes two arguments (exception, future). Exception will be the exception to handle and
        future will be an instance of asyncio.Future

    Examples
    --------
    >>> import asyncio
    >>> from pypresence import AioClient
    >>> RPC = AioClient("client_id")
    >>> async def main():
    ...     await RPC.start()
    ...     await RPC.set_activity(state="Playing a game", details="In the main menu")
    ...     RPC.close()
    >>> asyncio.run(main())
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, isasync=True)
        self._closed = False
        self._events = {}

    async def register_event(self, event: str, func: Callable, args=None):
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

    async def unregister_event(self, event: str, args=None):
        if args is None:
            args = {}
        event = event.lower()
        if event not in self._events:
            raise EventNotFound(event)
        await self.unsubscribe(event, args)
        del self._events[event]

    # noinspection PyProtectedMember
    def on_event(self, data):
        if self.sock_reader._eof:
            raise PyPresenceException("feed_data after feed_eof")
        if not data:
            return
        self.sock_reader._buffer.extend(data)
        self.sock_reader._wakeup_waiter()
        if (
            self.sock_reader._transport is not None
            and not self.sock_reader._paused
            and len(self.sock_reader._buffer) > 2 * self.sock_reader._limit
        ):
            try:
                self.sock_reader._transport.pause_reading()
            except NotImplementedError:
                self.sock_reader._transport = None
            else:
                self.sock_reader._paused = True

        payload = json.loads(data[8:].decode("utf-8"))

        if payload["evt"] is not None:
            evt = payload["evt"].lower()
            if evt in self._events:
                asyncio.create_task(self._events[evt](payload["data"]))
            elif evt == "error":
                raise DiscordError(payload["data"]["code"], payload["data"]["message"])

    async def authorize(self, client_id: str, scopes: List[str]):
        payload = Payload.authorize(client_id, scopes)
        self.send_data(1, payload)
        return await self.read_output()

    async def authenticate(self, token: str):
        payload = Payload.authenticate(token)
        self.send_data(1, payload)
        return await self.read_output()

    async def get_guilds(self):
        payload = Payload.get_guilds()
        self.send_data(1, payload)
        return await self.read_output()

    async def get_guild(self, guild_id: str):
        payload = Payload.get_guild(guild_id)
        self.send_data(1, payload)
        return await self.read_output()

    async def get_channel(self, channel_id: str):
        payload = Payload.get_channel(channel_id)
        self.send_data(1, payload)
        return await self.read_output()

    async def get_channels(self, guild_id: str):
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
    ):
        payload = Payload.set_user_voice_settings(
            user_id, pan_left, pan_right, volume, mute
        )
        self.send_data(1, payload)
        return await self.read_output()

    async def select_voice_channel(self, channel_id: str):
        payload = Payload.select_voice_channel(channel_id)
        self.send_data(1, payload)
        return await self.read_output()

    async def get_selected_voice_channel(self):
        payload = Payload.get_selected_voice_channel()
        self.send_data(1, payload)
        return await self.read_output()

    async def select_text_channel(self, channel_id: str):
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
    ):
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

    async def clear_activity(self, pid: int = os.getpid()):
        payload = Payload.set_activity(pid, activity=None)
        self.send_data(1, payload)
        return await self.read_output()

    async def subscribe(self, event: str, args=None):
        if args is None:
            args = {}
        payload = Payload.subscribe(event, args)
        self.send_data(1, payload)
        return await self.read_output()

    async def unsubscribe(self, event: str, args=None):
        if args is None:
            args = {}
        payload = Payload.unsubscribe(event, args)
        self.send_data(1, payload)
        return await self.read_output()

    async def get_voice_settings(self):
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
    ):
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

    async def capture_shortcut(self, action: str):
        payload = Payload.capture_shortcut(action)
        self.send_data(1, payload)
        return await self.read_output()

    async def send_activity_join_invite(self, user_id: str):
        payload = Payload.send_activity_join_invite(user_id)
        self.send_data(1, payload)
        return await self.read_output()

    async def close_activity_request(self, user_id: str):
        payload = Payload.close_activity_request(user_id)
        self.send_data(1, payload)
        return await self.read_output()

    def close(self):
        self.send_data(2, {"v": 1, "client_id": self.client_id})
        self.sock_writer.close()
        self._closed = True
        self.loop.close()

    async def start(self):
        await self.handshake()

    async def read(self):
        return await self.read_output()
