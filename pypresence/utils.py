"""Util functions that are needed but messy."""
import asyncio
import json
from enum import Enum
import time
import os
import sys

from .exceptions import PyPresenceException


PremiumType = Enum('PremiumType', {'None': 0, 'Nitro Classic': 1, 'Nitro': 2})


class UserFlags(Enum):
    # shamelessly ripped from discord.py's enums.py
    staff = 1
    partner = 2
    hypesquad = 4
    bug_hunter = 8
    mfa_sms = 16
    premium_promo_dismissed = 32
    hypesquad_bravery = 64
    hypesquad_brilliance = 128
    hypesquad_balance = 256
    early_supporter = 512
    team_user = 1024
    system = 4096
    has_unread_urgent_messages = 8192
    bug_hunter_level_2 = 16384
    verified_bot = 65536
    verified_bot_developer = 131072
    discord_certified_moderator = 262144


class PartialUser:
    def __init__(self, data):
        self._update(data)

    def _update(self, data):
        self._id = data.get('id')
        self._username = data.get('username')
        self._discriminator = data.get('discriminator')
        avatar = data.get('avatar')
        self._avatar = f'https://cdn.discordapp.com/avatars/{self._id}/{avatar}' if avatar else f'https://cdn.discordapp.com/embed/avatars/{self._discriminator % 5}.png'
        self._flags = data.get('flags',0)
        self._premium_type = PremiumType(data.get('premium_type',0))

    @property
    def id(self):
        return self._id

    @property
    def username(self):
        return self._username

    @property
    def discriminator(self):
        return self._discriminator

    @property
    def avatar(self):
        return self._avatar

    @property
    def premium_type(self):
        return self._premium_type

    @property
    def flags(self):
        return [flag for flag in UserFlags if self.has_flag(flag)]

    def has_flag(self, flag: UserFlags):
        return (self._flags & flag.value) == flag.value


# Made by https://github.com/LewdNeko ;^)
def remove_none(d: dict):
    for item in d.copy():
        if isinstance(d[item], dict):
            if len(d[item]):
                d[item] = remove_none(d[item])
            if not len(d[item]):
                del d[item]
        elif d[item] is None:
            del d[item]
    return d


# Returns on first IPC pipe matching Discord's
def get_ipc_path(pipe=None):
    ipc = 'discord-ipc-'
    if pipe:
        ipc = f"{ipc}{pipe}"

    if sys.platform == 'linux' or sys.platform == 'darwin':
        tempdir = (os.environ.get('XDG_RUNTIME_DIR') or tempfile.gettempdir())
        paths = ['.', 'snap.discord', 'app/com.discordapp.Discord']
    elif sys.platform == 'win32':
        tempdir = r'\\?\pipe'
        paths = ['.']
    else:
        return
    
    for path in paths:
        full_path = os.path.abspath(os.path.join(tempdir, path))
        if sys.platform == 'win32' or os.path.isdir(full_path):
            for entry in os.scandir(full_path):
                if entry.name.startswith(ipc):
                    return entry.path


def get_event_loop(force_fresh=False):
    if sys.platform == 'linux' or sys.platform == 'darwin':
        if force_fresh:
            return asyncio.new_event_loop()
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            return asyncio.new_event_loop()
        return loop
    elif sys.platform == 'win32':
        if force_fresh:
            return asyncio.ProactorEventLoop()
        loop = asyncio.get_event_loop()
        if isinstance(loop, asyncio.ProactorEventLoop) and not loop.is_closed():
            return loop
        return asyncio.ProactorEventLoop()


# This code used to do something. I don't know what, though.
try:  # Thanks, Rapptz :^)
    create_task = asyncio.ensure_future
except AttributeError:
    create_task = getattr(asyncio, "async")
    # No longer crashes Python 3.7
