import json
import os
import time

from .baseclient import BaseClient
from .payloads import Payload
from .utils import get_event_loop


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
               match: str = None, buttons: list = None,
               instance: bool = True, payload_override: dict = None):

        # Check if we're connected before attempting to update
        if self.sock_writer is None:
            return None

        if payload_override is None:
            payload = Payload.set_activity(pid=pid, state=state, details=details, start=start, end=end,
                                           large_image=large_image, large_text=large_text,
                                           small_image=small_image, small_text=small_text, party_id=party_id,
                                           party_size=party_size, join=join, spectate=spectate,
                                           match=match, buttons=buttons, instance=instance, activity=True)
        else:
            payload = payload_override
            
        try:
            self.send_data(1, payload)
            return self.loop.run_until_complete(self.read_output())
        except Exception:
            return None

    def clear(self, pid: int = os.getpid()):
        """Clear the current activity"""
        if self.sock_writer is None:
            return None
            
        try:
            payload = Payload.set_activity(pid, activity=None)
            self.send_data(1, payload)
            return self.loop.run_until_complete(self.read_output())
        except Exception:
            return None

    def connect(self):
        """
        Connect to Discord.
        
        Returns:
            bool: True if connection was successful, False otherwise.
        """
        try:
            self.update_event_loop(get_event_loop())
            self.loop.run_until_complete(self.handshake())
            return True
        except Exception:
            return False

    def close(self):
        """Safely close the connection to Discord"""
        try:
            if self.sock_writer:
                self.send_data(2, {'v': 1, 'client_id': self.client_id})
                self.loop.run_until_complete(super().close())
        except Exception:
            pass


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
                     match: str = None, buttons: list = None,
                     instance: bool = True):
        # Check if we're connected before attempting to update
        if self.sock_writer is None:
            return None
            
        try:
            payload = Payload.set_activity(pid=pid, state=state, details=details, start=start, end=end,
                                           large_image=large_image, large_text=large_text,
                                           small_image=small_image, small_text=small_text, party_id=party_id,
                                           party_size=party_size, join=join, spectate=spectate,
                                           match=match, buttons=buttons, instance=instance, activity=True)
            self.send_data(1, payload)
            return await self.read_output()
        except Exception:
            return None

    async def clear(self, pid: int = os.getpid()):
        """Clear the current activity"""
        if self.sock_writer is None:
            return None
            
        try:
            payload = Payload.set_activity(pid, activity=None)
            self.send_data(1, payload)
            return await self.read_output()
        except Exception:
            return None

    async def connect(self):
        """
        Connect to Discord.
        
        Returns:
            bool: True if connection was successful, False otherwise.
        """
        try:
            self.update_event_loop(get_event_loop())
            await self.handshake()
            return True
        except Exception:
            return False

    async def close(self):
        """Safely close the connection to Discord"""
        try:
            if self.sock_writer:
                self.send_data(2, {'v': 1, 'client_id': self.client_id})
                await super().close()
        except Exception:
            pass
