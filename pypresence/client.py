import inspect
import json
import os
from typing import List

from .baseclient import BaseClient
from .exceptions import *
from .payloads import Payload


class Client(BaseClient):
    def __init__(self, client_id: str, pipe: int = 0, loop=None, handler=None):
        """
        Creates the RPC client ready for usage.
        :param client_id: (str) OAuth2 App ID (found at https://discordapp.com/developers/applications/me)
        :param pipe: (int) Pipe that should be used to connect to the Discord client. Defaults to 0, can be 0-9
        :param loop: (asyncio.BaseEventLoop) Your own event loop (if you have one) that PyPresence should use.
                     One will be created if not supplied.
                     Information at https://docs.python.org/3/library/asyncio-eventloop.html
        :param handler: (function) The exception handler pypresence should send asynchronous errors to.
                                   This can be a coroutine or standard function as long as it takes two arguments
                                   (exception, future). Exception will be the exception to handle and future will be
                                   an instance of asyncio.Future
        """
        super().__init__(client_id, pipe=pipe, loop=loop, handler=handler)
        self._closed = False
        self._events = {}

    def register_event(self, event: str, func: callable, args: dict = {}):
        """
        Hook an event to a function. The function will be called whenever Discord sends that event. Will auto subscribe to it.
        :param event: (str) the event to hook
        :param func: (function) the function to pair with the event
        :param args: (dict) optional args used in subscription
        :return: pypresence.Response
        """
        if inspect.iscoroutinefunction(func):
            raise NotImplementedError
        elif len(inspect.signature(func).parameters) != 1:
            raise ArgumentError
        self.subscribe(event, args)
        self._events[event.lower()] = func

    def unregister_event(self, event: str, args: dict = {}):
        """
        Unhook an event from a function. Will auto unsubscribe from the event as well.
        :param event: (str) the event to unhook
        :param args: (dict) optional args used in unsubscription
        :return: pypresence.Response
        """
        event = event.lower()
        if event not in self._events:
            raise EventNotFound
        self.unsubscribe(event, args)
        del self._events[event]

    def on_event(self, data):
        """
        TODO
        :param data:
        :return:
        """
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

    def authorize(self, client_id: str, scopes: List[str]):
        """
        Used to authenticate a new client with your app.
        By default this pops up a modal in-app that asks the user to authorize access to your app.
        :param client_id: (str) OAuth2 application id
        :param scopes: (List) a list of OAuth scopes as strings see https://discordapp.com/developers/docs/topics/oauth2
        :return: pypresence.Response
        """
        payload = Payload.authorize(client_id, scopes)
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def authenticate(self, token: str):
        """
        Used to authenticate an existing client with your app.
        :param token: (int) OAuth2 access token
        :return: pypresence.Response
        """
        payload = Payload.authenticate(token)
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def get_guilds(self):
        """
        Used to get a list of guilds the client is in.
        :return: pypresence.Response
        """
        payload = Payload.get_guilds()
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def get_guild(self, guild_id: str):
        """

        :param guild_id:
        :return:
        """
        payload = Payload.get_guild(guild_id)
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def get_channel(self, channel_id: str):
        payload = Payload.get_channel(channel_id)
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def get_channels(self, guild_id: str):
        """
        Used to get a guild’s channels the client is in.
        :param guild_id: TODO
        :return: pypresence.Response
        """
        payload = Payload.get_channels(guild_id)
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def set_user_voice_settings(self, user_id: str, pan_left: float = None,
                                pan_right: float = None, volume: int = None,
                                mute: bool = None):
        """
        Used to get a channel the client is in.
        :param user_id: (str) user id
        :param pan_left: (float) left pan of the user
        :param pan_right: (float) right pan of the user
        :param volume: (int) the volume of user (defaults to 100, min 0, max 200)
        :param mute: (bool) the mute state of the user
        :return: pypresence.Response
        """
        payload = Payload.set_user_voice_settings(user_id, pan_left, pan_right, volume, mute)
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def select_voice_channel(self, channel_id: str):
        """
        Used to join and leave voice channels, group dms, or dms.
        :param channel_id: (str) channel id to join (or None to leave)
        :return: pypresence.Response
        """
        payload = Payload.select_voice_channel(channel_id)
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def get_selected_voice_channel(self):
        """
        Used to get the client’s current voice channel.
        :return: pypresence.Response
        """
        payload = Payload.get_selected_voice_channel()
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def select_text_channel(self, channel_id: str):
        """
        Used to join and leave text channels, group dms, or dms.
        :param channel_id: (str) channel id to join (or None to leave)
        :return: 	pypresence.Response
        """
        payload = Payload.select_text_channel(channel_id)
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def set_activity(self, pid: int = os.getpid(),
                     state: str = None, details: str = None,
                     start: int = None, end: int = None,
                     large_image: str = None, large_text: str = None,
                     small_image: str = None, small_text: str = None,
                     party_id: str = None, party_size: list = None,
                     join: str = None, spectate: str = None,
                     match: str = None, instance: bool = True):
        """
        Used to set the activity shown on Discord profiles and status of users. Takes the following as parameters.
        :param pid: (int) the process id of your game
        :param state: (str) the user’s current status
        :param details: (str) what the player is currently doing
        :param start: (int) epoch time for game start
        :param end: (int) epoch time for game end
        :param large_image: (str) name of the uploaded image for the large profile artwork
        :param large_text: (str) tooltip for the large image
        :param small_image: (str) name of the uploaded image for the small profile artwork
        :param small_text: (str) tootltip for the small image
        :param party_id: (str) id of the player’s party, lobby, or group
        :param party_size: (list) current size of the player’s party, lobby, or group, and the max in this format: [1,4]
        :param join: (str) unique hashed string for chat invitations and ask to join
        :param spectate: (str) unique hashed string for spectate button
        :param match: (str) unique hashed string for spectate and join
        :param instance: (bool) marks the match as a game session with a specific beginning and end
        :return: pypresence.Response
        """
        payload = Payload.set_activity(pid, state, details, start, end, large_image, large_text,
                                       small_image, small_text, party_id, party_size, join, spectate,
                                       match, instance, activity=True)
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def clear_activity(self, pid: int = os.getpid()):
        """
        Clear the activity.
        :param pid: (int) the process id of your game
        :return:
        """
        payload = Payload.set_activity(pid, activity=None)
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def subscribe(self, event: str, args: dict = {}):
        """
        Used to subscribe to events.
        :param event: (str) event name to subscribe to
        :param args: (dict) any args to go along with the event
        :return: pypresence.Response
        """
        payload = Payload.subscribe(event, args)
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def unsubscribe(self, event: str, args: dict = {}):
        """
        Used to unsubscribe from events
        :param event: (str) event name to unsubscribe from
        :param args: (dict) any args to go along with the event
        :return: pypresence.Response
        """
        payload = Payload.unsubscribe(event, args)
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def get_voice_settings(self):
        """
        Get the user’s voice settings.
        :return: pypresence.Response
        """
        payload = Payload.get_voice_settings()
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def set_voice_settings(self, _input: dict = None, output: dict = None,
                           mode: dict = None, automatic_gain_control: bool = None,
                           echo_cancellation: bool = None, noise_suppression: bool = None,
                           qos: bool = None, silence_warning: bool = None,
                           deaf: bool = None, mute: bool = None):
        """
        Set the user’s voice settings.
        :param _input: (dict) input settings
        :param output: (dict) output settings
        :param mode: (dict) voice mode settings
        :param automatic_gain_control: (bool) state of automatic gain control
        :param echo_cancellation: (bool) state of echo cancellation
        :param noise_suppression: (bool) state of noise suppression
        :param qos: (bool) state of voice quality of service
        :param silence_warning: (bool) state of silence warning notice
        :param deaf: (bool) state of self-deafen
        :param mute: (bool) state of self-mute
        :return: pypresence.Response
        """
        payload = Payload.set_voice_settings(_input, output, mode, automatic_gain_control, echo_cancellation,
                                             noise_suppression, qos, silence_warning, deaf, mute)
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def capture_shortcut(self, action: str):
        """
        Used to capture a keyboard shortcut entered by the user.
        :param action: (str) capture action, either 'START' or 'STOP'
        :return: pypresence.Response
        """
        payload = Payload.capture_shortcut(action)
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def send_activity_join_invite(self, user_id: str):
        """
        Used to accept an Ask to Join request.
        :param user_id: (str) user id
        :return: pypresence.Response
        """
        payload = Payload.send_activity_join_invite(user_id)
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def close_activity_request(self, user_id: str):
        """
        Used to reject an Ask to Join request.
        :param user_id: (str) user id
        :return: pypresence.Response
        """
        payload = Payload.close_activity_request(user_id)
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def close(self):
        """
        Closes the connection.
        :return:
        """
        self.send_data(2, {'v': 1, 'client_id': self.client_id})
        self.sock_writer.close()
        self._closed = True
        self.loop.close()

    def start(self):
        """
        Initializes the connection - must be done in order to run RPC commands.
        :return: pypresence.Response
        """
        self.loop.run_until_complete(self.handshake())

    def read(self):
        return self.loop.run_until_complete(self.read_output())


class AioClient(BaseClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, isasync=True)
        self._closed = False
        self._events = {}

    async def register_event(self, event: str, func: callable, args: dict = {}):
        if not inspect.iscoroutinefunction(func):
            raise InvalidArgument('Coroutine', 'Subroutine', 'Event function must be a coroutine')
        elif len(inspect.signature(func).parameters) != 1:
            raise ArgumentError
        await self.subscribe(event, args)
        self._events[event.lower()] = func

    async def unregister_event(self, event: str, args: dict = {}):
        event = event.lower()
        if event not in self._events:
            raise EventNotFound
        await self.unsubscribe(event, args)
        del self._events[event]

    async def on_event(self, data):
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
                await self._events[evt](payload["data"])
            elif evt == 'error':
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

    async def set_user_voice_settings(self, user_id: str, pan_left: float = None,
                                      pan_right: float = None, volume: int = None,
                                      mute: bool = None):
        payload = Payload.set_user_voice_settings(user_id, pan_left, pan_right, volume, mute)
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

    async def set_activity(self, pid: int = os.getpid(),
                           state: str = None, details: str = None,
                           start: int = None, end: int = None,
                           large_image: str = None, large_text: str = None,
                           small_image: str = None, small_text: str = None,
                           party_id: str = None, party_size: list = None,
                           join: str = None, spectate: str = None,
                           match: str = None, instance: bool = True):
        payload = Payload.set_activity(pid, state, details, start, end, large_image, large_text,
                                       small_image, small_text, party_id, party_size, join, spectate,
                                       match, instance, activity=True)
        self.send_data(1, payload)
        return await self.read_output()

    async def clear_activity(self, pid: int = os.getpid()):
        payload = Payload.set_activity(pid, activity=None)
        self.send_data(1, payload)
        return await self.read_output()

    async def subscribe(self, event: str, args: dict = {}):
        payload = Payload.subscribe(event, args)
        self.send_data(1, payload)
        return await self.read_output()

    async def unsubscribe(self, event: str, args: dict = {}):
        payload = Payload.unsubscribe(event, args)
        self.send_data(1, payload)
        return await self.read_output()

    async def get_voice_settings(self):
        payload = Payload.get_voice_settings()
        self.send_data(1, payload)
        return await self.read_output()

    async def set_voice_settings(self, _input: dict = None, output: dict = None,
                                 mode: dict = None, automatic_gain_control: bool = None,
                                 echo_cancellation: bool = None, noise_suppression: bool = None,
                                 qos: bool = None, silence_warning: bool = None,
                                 deaf: bool = None, mute: bool = None):
        payload = Payload.set_voice_settings(_input, output, mode, automatic_gain_control, echo_cancellation,
                                             noise_suppression, qos, silence_warning, deaf, mute)
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
        self.send_data(2, {'v': 1, 'client_id': self.client_id})
        self.sock_writer.close()
        self._closed = True
        self.loop.close()

    async def start(self):
        await self.handshake()

    async def read(self):
        return await self.read_output()
