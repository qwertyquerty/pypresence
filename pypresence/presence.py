import os
import asyncio
from .baseclient import BaseClient
from .payloads import Payload


class Presence(BaseClient):

    def __init__(self, client_id: str, pipe: int = 0, loop: asyncio.BaseEventLoop = None, handler=None):
        """
        :param client_id: (str) OAuth2 App ID (found at https://discordapp.com/developers/applications/me)
        :param pipe: (int) Pipe that should be used to connect to the Discord client. Defaults to 0, can be 0-9
        :param loop: (asyncio.BaseEventLoop) Your own event loop (if you have one) that PyPresence should use.
                     One will be created if not supplied.
                     Information at https://docs.python.org/3/library/asyncio-eventloop.html
        :param handler: (function) The exception handler pypresence should send asynchronous errors to.
                        This can be a coroutine or standard function as long as it takes two arguments
                        (exception, future).
                        Exception will be the exception to handle and future will be an instance of asyncio.Future
        """
        super().__init__(client_id, pipe=pipe, loop=loop, handler=handler)

    def update(self, pid: int = os.getpid(),
               state: str = None, details: str = None,
               start: int = None, end: int = None,
               large_image: str = None, large_text: str = None,
               small_image: str = None, small_text: str = None,
               party_id: str = None, party_size: list = None,
               join: str = None, spectate: str = None,
               match: str = None, instance: bool = True,
               _donotuse=True):
        """
        Sets the user’s presence on Discord.
        :param pid: (int) the process id of your game
        :param state: (str) the user’s current status
        :param details: (str) what the player is currently doing
        :param start: (int) epoch time for game start
        :param end:  (int) epoch time for game end
        :param large_image: (str) name of the uploaded image for the large profile artwork
        :param large_text: (str) tooltip for the large image
        :param small_image: (str) name of the uploaded image for the small profile artwork
        :param small_text: (str) tootltip for the small image
        :param party_id: (str) id of the player’s party, lobby, or group
        :param party_size: (List) current size of the player’s party, lobby, or group, and the max in this format: [1,4]
        :param join: (str) unique hashed string for chat invitations and ask to join
        :param spectate: (str) unique hashed string for spectate button
        :param match: (str) unique hashed string for spectate and join
        :param instance: (bool) marks the match as a game session with a specific beginning and end
        :param _donotuse:  (bool) undocumented
        :return: pypresence.Response
        """

        if _donotuse is True:
            payload = Payload.set_activity(pid, state, details, start, end, large_image, large_text,
                                           small_image, small_text, party_id, party_size, join, spectate,
                                           match, instance, activity=True)
        else:
            payload = _donotuse
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def clear(self, pid: int = os.getpid()):
        """
        Clears the presence.
        :param pid: (int) the process id of your game
        :return: pypresence.Response
        """
        payload = Payload.set_activity(pid, activity=None)
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def connect(self):
        """
        Initializes the connection - must be done in order to make any updates to Rich Presence.
        :return: pypresence.Response
        """
        self.update_event_loop(self.get_event_loop())
        self.loop.run_until_complete(self.handshake())

    def close(self):
        """
        Closes the connection.
        :return: pypresence.Response
        """
        self.send_data(2, {'v': 1, 'client_id': self.client_id})
        self.sock_writer.close()
        self.loop.close()


class AioPresence(BaseClient):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, isasync=True)

    async def update(self, pid: int = os.getpid(),
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

    async def clear(self, pid: int = os.getpid()):
        payload = Payload.set_activity(pid, activity=None)
        self.send_data(1, payload)
        return await self.read_output()

    async def connect(self):
        self.update_event_loop(self.get_event_loop())
        await self.handshake()

    def close(self):
        self.send_data(2, {'v': 1, 'client_id': self.client_id})
        self.sock_writer.close()
        self.loop.close()
