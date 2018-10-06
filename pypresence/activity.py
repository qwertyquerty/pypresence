import os
from typing import Union

from .payloads import Payload
from .presence import Presence, AioPresence


class Activity:

    def __init__(self, pid: int = os.getpid(),
                 state: str = None, details: str = None,
                 start: int = None, end: int = None,
                 large_image: str = None, large_text: str = None,
                 small_image: str = None, small_text: str = None,
                 party_id: str = None, party_size: list = None,
                 join: str = None, spectate: str = None,
                 match: str = None, instance: bool = True, activity: Union[bool, None] = True,
                 client: Union[Presence, AioPresence] = None):

        self.payload = Payload.set_activity(pid, state, details, start, end, large_image, large_text,
                                            small_image, small_text, party_id, party_size, join, spectate,
                                            match, instance, activity)
        if client is not None:
            self.client = client

    def __set__(self):
        pass

# This idea is a WIP. Pushing
# Not sure on the name / intended functionality of this
# it'd be fine if we just added this functionality to pypresence.Presence