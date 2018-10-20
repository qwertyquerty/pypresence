import os
from time import time

from .payloads import Payload
from .presence import Presence
from .response import Response
from .utils import remove_none


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

        self.p_properties = ('pid', 'state', 'details', 'start', 'end', 'large_image', 'large_text', 'small_image', 'small_text', 'party_id', 'party_size', 'join', 'spectate', 'match', 'instance')
        self.response = Response.from_dict(self.payload.data)

        if not isinstance(client, Presence):
            raise NotImplementedError
        self.client = client

    def __setattr__(self, name, value):
        p = getattr(self, 'p_properties', None)
        r = getattr(self, 'response', None)
        if p and name in p:
            r.set_prop(name,value)

            payload = remove_none(self.response.to_dict())

            self.client.update(_donotuse=payload)
        else:
            self.__dict__[name] = value


    def __getattr__(self, name):
        p = object.__getattribute__(self, 'p_properties')
        r = object.__getattribute__(self, 'response')
        if p and name in p:
            return r.get_prop(name)

        return getattr(self, name, None)

    def started_at(self, seconds_ago: int):
        if seconds_ago < 0 or not isinstance(seconds_ago, int):
            raise PyPresenceException('Must be a positive integer of how many seconds it has been since the start of the activity.')
        self.start = int(time()) - seconds_ago

    def end_in(self, time_until_end: int):
        if time_until_end < 0 or not isinstance(time_until_end, int):
            raise PyPresenceException('Must be a positive integer of how many seconds the activity will end in.')
        self.end = int(time()) + time_until_end

# This SHOULD work, but is untested. Currently unsure if how I've done
# this is "right"... When you do Activity.state = 'my state here', it
# should call Presence.update() with a working payload. Had to do a bit
# of a hack to make it easier and ended up easing the Response class because it
