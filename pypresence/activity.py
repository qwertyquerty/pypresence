import os

from .payloads import Payload
from .presence import Presence
from .response import Response


class Activity:

    def __init__(self, client: Presence, pid: int = os.getpid(),
                 state: str = None, details: str = None,
                 start: int = None, end: int = None,
                 large_image: str = None, large_text: str = None,
                 small_image: str = None, small_text: str = None,
                 party_id: str = None, party_size: list = None,
                 join: str = None, spectate: str = None,
                 match: str = None, instance: bool = True):

        self.payload = Payload.set_activity(pid, state, details, start, end, large_image, large_text,
                                            small_image, small_text, party_id, party_size, join, spectate,
                                            match, instance, _rn=False)
        self.response = Response.from_dict(self.payload.data)
        if not isinstance(client, Presence):
            raise NotImplementedError
        self.client = client

    def __setattr__(self, name, value):
        if name in self.response.properties:
            setattr(self.response, name, value)
            payload = self.response.to_dict()
            self.client.update(_donotuse=payload)
        else:
            setattr(self, name, value)
            
    def __getattr__(self, name):
        if name in self.response.properties:
            return getattr(self.response, name)
        else:
            return self.name

# This SHOULD work, but is untested. Currently unsure if how I've done
# this is "right"... When you do Activity.state = 'my state here', it
# should call Presence.update() with a working payload. Had to do a bit
# of a hack to make it easier and ended up easing the Response class because it
