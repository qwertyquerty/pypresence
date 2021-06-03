"""Util functions that are needed but messy."""
import asyncio
import json
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


# Don't call these. Ever.
def _load_payloads(filename):
    with open(filename, 'r') as fp:
        f = fp.read()

    payloaddict = {}
    for line in f.splitlines():
        name, payload = line.split('||')
        payloaddict[name] = payload

    return payloaddict


def _payload_gen(payload_type: str, payload_params: dict):
    payloads = _load_payloads('pllist.NEKO')  # dont like txt files
    if payload_type.upper() not in payloads:
        raise PyPresenceException('Payload type not supported or does not exist.')
    payload_str = payloads[payload_type]
    for key, value in payload_params.items():
        payload_str.replace(";;{0};;".format(key), value)

    payload = json.loads(payload_str)
    payload["nonce"] = payload["nonce"].format(time.time())


# This code used to do something. I don't know what, though.
try:  # Thanks, Rapptz :^)
    create_task = asyncio.ensure_future
except AttributeError:
    create_task = getattr(asyncio, "async")
    # No longer crashes Python 3.7
