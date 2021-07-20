from typing import Optional, List, Dict
import os
import warnings

from .baseclient import BaseClient
from .client import Client, AioClient
from .presence import Presence, AioPresence


class InvalidActivityWarning(UserWarning):
    pass


class ActivityProperty:
    def __init__(self, default=None):
        self.default = default

    def __set_name__(self, owner, name):
        self.private_name = f'_{name}'

    def __get__(self, instance, owner):
        return getattr(instance, self.private_name, None) or self.default

    def __set__(self, instance, value):
        setattr(instance, self.private_name, value)
        if instance.autoupdate:
            instance.update()

    def __delete__(self, instance):
        setattr(instance, self.private_name, None)
        if instance.autoupdate:
            instance.update()


class Activity:
    r"""The Activity class is an ease-of-use beginner-friendly interface,
    capable of being attached to any instance of :class:`BaseClient`.
    """

    def __init__(self, client_id: str = None, client: BaseClient = None, autoupdate: bool = True):
        """
        You must pass either `client_id` or `client`. Passing both will prioritise the `client` param.

        Parameters
        -----------
        client_id: Optional[:class:`str`]
            The Discord Client ID of the Application that we are connecting as
        client: Optional[:class:`BaseClient`]
            Any instance of BaseClient (Client, AioClient, Presence, AioPresence)
        autoupdate: Optional[:class:`bool`]
            Whether updating the attributes of the Activity class cause an update to Discord.
        """
        if client_id is None and client is None:
            raise ValueError('You must pass either `client_id` or `client` to create an Activity class')
        if client_id and client is None:
            client = Client(client_id)
            client.start()
        self._client: Optional[BaseClient] = client
        self._excluded_methods = ['to_json', 'from_json', 'update', 'attach', 'add_button', 'clear_buttons',
                                  'autoupdate']
        self.autoupdate = autoupdate

    def _is_public_attr(self, attr: str) -> bool:
        return not attr.startswith('_') and attr not in self._excluded_methods

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

    def to_json(self) -> dict:
        """Converts the class to a :class:`dict` that can be passed to the client for updating the presence.

        Returns
        --------
        :class:`dict`
            The dictionary representation of this class
        """
        return {
            attr: getattr(self, attr, None)
            for attr in dir(self)
            if self._is_public_attr(attr)
        }

    @classmethod
    def from_json(cls, client_id: str = None, client: BaseClient = None, **kwargs):
        c = cls(client_id=client_id, client=client)
        for k, v in kwargs.items():
            if c._is_public_attr(k):
                setattr(c, k, v)
        return c

    def update(self) -> None:
        """
        Updates the bound client with the data that has been assigned to this instance.
        """
        if not self._client:
            return
        if not self.state:
            warnings.warn('A valid activity requires that the state parameter be set! Make sure that the state is '
                          'set first, or Discord won\'t allow the Rich Presence to show!', InvalidActivityWarning)
            return
        kwargs = self.to_json()
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

    def attach(self, client: BaseClient) -> None:
        """
        Attaches this class to a Client and binds it for auto-updating.

        Parameters
        -----------
        client: :class:`BaseClient`
            Any instance of BaseClient (Client, AioClient, Presence, AioPresence)
        """
        self._client = client
        self.update()

    def add_button(self, label: str, url: str) -> None:
        """
        Adds a button to the presence.

        Parameters
        -----------
        label: :class:`str`
            The label that shows on the button as text.
        url: :class:`str`
            The URL that clicking the button will take you to. Buttons are only clickable for other users.
        """
        data = {"label": label, "url": url}
        if len(self.buttons) >= 2:
            raise ValueError('A Rich Presence only allows up to 2 buttons')
        
        if isinstance(self.buttons, list):
            self.buttons.append(data)
        else:
            self.buttons = [data]

    def clear_buttons(self) -> None:
        """
        Clears the buttons on the presence. Alias for `del activity.buttons`
        """
        self.buttons = []
