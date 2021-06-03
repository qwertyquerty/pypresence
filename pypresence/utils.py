"""Util functions that are needed but messy."""
import asyncio
import json
import time
import os
import sys

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

    if sys.platform == 'linux' or sys.platform == 'darwin':
        tempdir = (os.environ.get('XDG_RUNTIME_DIR') or tempfile.gettempdir())
        paths = ['.', 'snap.discord', 'app/com.discordapp.Discord']
    elif sys.platform == 'win32':
        tempdir = r'\\?\pipe'
        paths = ['.']
    
    for path in paths:
        full_path = os.path.abspath(os.path.join(tempdir,path))
        if sys.platform == 'win32' or os.path.isdir(full_path):
            for entry in os.scandir(full_path):
                if entry.name.startswith(ipc):
                    return entry.path
    
    return None


# This code used to do something. I don't know what, though.
try:  # Thanks, Rapptz :^)
    create_task = asyncio.ensure_future
except AttributeError:
    create_task = getattr(asyncio, "async")
    # No longer crashes Python 3.7
