"""Util functions that are needed but messy."""
import asyncio
import json
import os
import sys
import tempfile
import time

from .exceptions import PyPresenceException


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

    if sys.platform in ('linux', 'darwin'):
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
    if sys.platform in ('linux', 'darwin'):
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
