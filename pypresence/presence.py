import json
import logging
import os
from typing import Optional, List, Dict

from .baseclient import BaseClient
from .payloads import Payload
from .utils import get_event_loop


class Presence(BaseClient):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update(self, pid: int = os.getpid(),
               state: Optional[str] = None, details: Optional[str] = None,
               start: Optional[int] = None, end: Optional[int] = None,
               large_image: Optional[str] = None, large_text: Optional[str] = None,
               small_image: Optional[str] = None, small_text: Optional[str] = None,
               party_id: Optional[str] = None, party_size: Optional[List[int]] = None,
               join: Optional[str] = None, spectate: Optional[str] = None,
               match: Optional[str] = None, buttons: Optional[List[Dict[str, str]]] = None,
               instance: bool = True, payload_override: Optional[Dict] = None):

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
        except (ConnectionError, OSError) as e:
            logging.debug(f"Connection error in update: {e}")
            return None
        except Exception as e:
            logging.debug(f"Unexpected error in update: {e}")
            return None

    def clear(self, pid: int = os.getpid()):
        """Clear the current activity"""
        if self.sock_writer is None:
            return None
            
        try:
            payload = Payload.set_activity(pid, activity=None)
            self.send_data(1, payload)
            return self.loop.run_until_complete(self.read_output())
        except (ConnectionError, OSError) as e:
            logging.debug(f"Connection error in clear: {e}")
            return None
        except Exception as e:
            logging.debug(f"Unexpected error in clear: {e}")
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
        except (ConnectionError, OSError) as e:
            logging.debug(f"Connection error in connect: {e}")
            return False
        except Exception as e:
            logging.debug(f"Unexpected error in connect: {e}")
            return False

    def close(self):
        """Safely close the connection to Discord"""
        try:
            if self.sock_writer:
                self.send_data(2, {'v': 1, 'client_id': self.client_id})
                self.loop.run_until_complete(super().close())
        except (ConnectionError, OSError) as e:
            logging.debug(f"Connection error during close: {e}")
        except Exception as e:
            logging.debug(f"Unexpected error during close: {e}")


class AioPresence(BaseClient):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, isasync=True)

    async def update(self, pid: int = os.getpid(),
                     state: Optional[str] = None, details: Optional[str] = None,
                     start: Optional[int] = None, end: Optional[int] = None,
                     large_image: Optional[str] = None, large_text: Optional[str] = None,
                     small_image: Optional[str] = None, small_text: Optional[str] = None,
                     party_id: Optional[str] = None, party_size: Optional[List[int]] = None,
                     join: Optional[str] = None, spectate: Optional[str] = None,
                     match: Optional[str] = None, buttons: Optional[List[Dict[str, str]]] = None,
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
        except (ConnectionError, OSError) as e:
            logging.debug(f"Connection error in async update: {e}")
            return None
        except Exception as e:
            logging.debug(f"Unexpected error in async update: {e}")
            return None

    async def clear(self, pid: int = os.getpid()):
        """Clear the current activity"""
        if self.sock_writer is None:
            return None
            
        try:
            payload = Payload.set_activity(pid, activity=None)
            self.send_data(1, payload)
            return await self.read_output()
        except (ConnectionError, OSError) as e:
            logging.debug(f"Connection error in async clear: {e}")
            return None
        except Exception as e:
            logging.debug(f"Unexpected error in async clear: {e}")
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
        except (ConnectionError, OSError) as e:
            logging.debug(f"Connection error in async connect: {e}")
            return False
        except Exception as e:
            logging.debug(f"Unexpected error in async connect: {e}")
            return False

    async def close(self):
        """Safely close the connection to Discord"""
        try:
            if self.sock_writer:
                self.send_data(2, {'v': 1, 'client_id': self.client_id})
                await super().close()
        except (ConnectionError, OSError) as e:
            logging.debug(f"Connection error during async close: {e}")
        except Exception as e:
            logging.debug(f"Unexpected error during async close: {e}")
