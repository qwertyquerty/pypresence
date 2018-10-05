"""Util functions that are needed but messy."""
import asyncio


# Made by https://github.com/LewdNeko ;^)
def remove_none(d: dict):
    for item in d.copy():
        if isinstance(d[item], dict):
            if len(d[item]):
                d[item] = remove_none(d[item])
            else:
                del d[item]
        elif d[item] is None:
            del d[item]
    return d


# This code used to do something. I don't know what, though.
try: # Thanks, Rapptz :^)
    create_task = asyncio.ensure_future
except AttributeError:
    create_task = getattr(asyncio, "async")
    # No longer crashes Python 3.7
