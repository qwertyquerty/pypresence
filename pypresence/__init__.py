"""
Python RPC Client for Discord
-----------------------------
By: qwertyquerty and LewdNeko
"""

from .baseclient import BaseClient
from .client import AioClient, Client
from .exceptions import *
from .presence import AioPresence, Presence
from .types import ActivityType, StatusDisplayType

__title__ = "pypresence"
__author__ = "qwertyquerty"
__copyright__ = "Copyright 2018 - Current qwertyquerty"
__license__ = "MIT"
__version__ = "4.7.0-alpha.2"
