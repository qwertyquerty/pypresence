"""Util functions that are messy but needed."""
# import asyncio
import json
import time

from .exceptions import PyPresenceException


# Made by https://github.com/LewdNeko ;^)
def remove_none(d: dict):
    for key in d.keys():
        if isinstance(d[key], dict):
            if d[key]:
                remove_none(d[key])
            else:
                del d[key]
        elif d[key] is None:
            del d[key]


# Don't call these. Ever.
def _load_payloads(filename):
    with open(filename, 'r') as fp:
        lines = fp.read().splitlines()

    payload_dict = {}
    for line in lines:
        name, payload = line.split('||')
        payload_dict[name] = payload

    return payload_dict


def _payload_gen(payload_type: str, payload_params: dict):
    # why not use a JSON file?
    payloads = _load_payloads('pllist.NEKO')  # don't like txt files
    if payload_type.upper() not in payloads:
        raise PyPresenceException('Payload type not supported or does not exist.')
    payload_str = payloads[payload_type]
    for key, value in payload_params.items():
        payload_str.replace(";;{0};;".format(key), value)

    payload = json.loads(payload_str)
    payload["nonce"] = payload["nonce"].format(time.time())


# This code used to do something. I don't know what, though.
# try:  # Thanks, Rapptz :^)
#     create_task = asyncio.ensure_future
# except AttributeError:
#     create_task = getattr(asyncio, "async")
    # No longer crashes Python 3.7
