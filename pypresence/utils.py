"""Util functions that are needed but messy."""
import asyncio
import json
import os
import sys
import tempfile
import time
import warnings

from .exceptions import PyPresenceException


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

def test_ipc_path(path):
    '''Tests an IPC pipe to ensure that it actually works'''
    try:
        with open(path) as f:
            return True
    except Exception as e:
        warnings.warn(f"IPC pipe path {path.path} exists, but could not be opened because of {e}. Trying next pipe")
        return False
        

# Returns on first IPC pipe matching Discord's
def get_ipc_path(pipe=None):
    ipc = 'discord-ipc-'
    if pipe:
        ipc = f"{ipc}{pipe}"

    if sys.platform in ('linux', 'darwin'):
        tempdir = (os.environ.get('XDG_RUNTIME_DIR') or tempfile.gettempdir())
        paths = ['.', 'snap.discord', 'app/com.discordapp.Discord', 'app/com.discordapp.DiscordCanary']
    elif sys.platform == 'win32':
        tempdir = r'\\?\pipe'
        paths = ['.']
    else:
        return
    
    for path in paths:
        full_path = os.path.abspath(os.path.join(tempdir, path))
        if sys.platform == 'win32' or os.path.isdir(full_path):
            for entry in os.scandir(full_path):
                if entry.name.startswith(ipc) and os.path.exists(entry) and test_ipc_path(entry):
                    return entry.path


def get_event_loop(force_fresh=False):
    if force_fresh:
        return asyncio.new_event_loop()
    try:
        running = asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.new_event_loop()
    if running.is_closed():
        return asyncio.new_event_loop()
    return running
