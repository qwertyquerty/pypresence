"""
Python RPC Client for Discord
-----------------------------
By: qwertyquerty and LewdNeko
"""

from .baseclient import BaseClient
from .client import Client, AioClient
from .exceptions import *
from .presence import Presence, AioPresence
from .utils import ClientType


__title__ = 'pypresence'
__author__ = 'qwertyquerty'
__copyright__ = 'Copyright 2018 qwertyquerty'
__license__ = 'MIT'
__version__ = '4.2.1'
