from __future__ import annotations

import os
import sys

from .baseclient import BaseClient
from .payloads import Payload
from .types import ActivityType, StatusDisplayType
from .utils import get_event_loop


class Presence(BaseClient):
    """
    Discord Rich Presence Client.

    Creates a simple Rich Presence client for updating Discord activity status.

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
    >>> from pypresence import Presence
    >>> RPC = Presence("client_id")
    >>> RPC.connect()
    >>> RPC.update(state="Playing a game", details="In the main menu")
    """

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
        """
        Update the user's Discord Rich Presence.

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

        Examples
        --------
        >>> RPC.update(state="In Main Menu", details="Playing Solo")
        >>> RPC.update(
        ...     state="Playing a Game",
        ...     details="Level 5",
        ...     large_image="game_logo",
        ...     large_text="My Awesome Game",
        ...     buttons=[{"label": "View Game", "url": "https://example.com"}]
        ... )
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
        """
        Clear the Rich Presence.

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

    def connect(self):
        """
        Initialize the connection to Discord.

        This must be called before making any updates to Rich Presence.

        Returns
        -------
        None
        """
        self.update_event_loop(get_event_loop())
        self.loop.run_until_complete(self.handshake())

    def close(self):
        self.send_data(2, {"v": 1, "client_id": self.client_id})
        self.loop.close()
        if sys.platform == "win32":
            self.sock_writer._call_connection_lost(None)


class AioPresence(BaseClient):
    """
    Async Discord Rich Presence Client.

    Creates an asynchronous Rich Presence client for updating Discord activity status.
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
    >>> from pypresence import AioPresence
    >>> RPC = AioPresence("client_id")
    >>> async def main():
    ...     await RPC.connect()
    ...     await RPC.update(state="Playing a game", details="In the main menu")
    ...     await RPC.close()
    >>> asyncio.run(main())
    """

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
        """
        Update the user's Discord Rich Presence asynchronously.

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

        Returns
        -------
        Response
            The response from Discord

        Examples
        --------
        >>> await RPC.update(state="In Main Menu", details="Playing Solo")
        >>> await RPC.update(
        ...     state="Playing a Game",
        ...     details="Level 5",
        ...     large_image="game_logo",
        ...     large_text="My Awesome Game",
        ...     buttons=[{"label": "View Game", "url": "https://example.com"}]
        ... )
        """
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
        """
        Clear the Rich Presence asynchronously.

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
        return await self.read_output()

    async def connect(self):
        """
        Initialize the connection to Discord asynchronously.

        This must be called before making any updates to Rich Presence.

        Returns
        -------
        None
        """
        self.update_event_loop(get_event_loop())
        await self.handshake()

    def close(self):
        """
        Close the connection to Discord.

        Returns
        -------
        None
        """
        self.send_data(2, {"v": 1, "client_id": self.client_id})
        self.loop.close()
        if sys.platform == "win32":
            self.sock_writer._call_connection_lost(None)
