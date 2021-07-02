from typing import Optional, List, Dict
import os

from .baseclient import BaseClient
from .client import Client, AioClient
from .presence import Presence, AioPresence


# TODO: In-line documentation


class ActivityProperty:
    def __init__(self, default=None):
        self.default = default

    def __set_name__(self, owner, name):
        self.private_name = f'_{name}'

    def __get__(self, instance, owner):
        return getattr(instance, self.private_name, None) or self.default

    def __set__(self, instance, value):
        setattr(instance, self.private_name, value)
        instance.update()

    def __delete__(self, instance):
        setattr(instance, self.private_name, None)
        instance.update()


class Activity:
    def __init__(self, client: Optional[BaseClient] = None):
        self._client: Optional[BaseClient] = client
        self._excluded_methods = ['json', 'update', 'attach']

    pid: int = ActivityProperty(os.getpid())
    state: str = ActivityProperty()
    details: str = ActivityProperty()
    start: int = ActivityProperty()
    end: int = ActivityProperty()
    large_image: str = ActivityProperty()
    large_text: str = ActivityProperty()
    small_image: str = ActivityProperty()
    small_text: str = ActivityProperty()
    party_id: str = ActivityProperty()
    party_size: List[int] = ActivityProperty()
    join: str = ActivityProperty()
    spectate: str = ActivityProperty()
    match: str = ActivityProperty()
    buttons: List[Dict[str, str]] = ActivityProperty()
    instance: bool = ActivityProperty(True)

    def json(self):
        return {
            attr: getattr(self, attr, None)
            for attr in dir(self)
            if not attr.startswith('_')
            and attr not in self._excluded_methods
        }

    def update(self):
        if not self._client:
            return
        kwargs = self.json()
        if isinstance(self._client, (AioClient, AioPresence)):
            _future = self._client.set_activity(**kwargs) if isinstance(self._client, AioClient) else \
                self._client.update(**kwargs)
            self._client.loop.run_until_complete(_future)
        elif isinstance(self._client, Client):
            self._client.set_activity(**kwargs)
        elif isinstance(self._client, Presence):
            self._client.update(**kwargs)
        else:
            raise ValueError('Unexpected client type found')

    def attach(self, client: BaseClient):
        self._client = client
        self.update()
