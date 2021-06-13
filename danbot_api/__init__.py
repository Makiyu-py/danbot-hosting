from collections import namedtuple

from .client import DanBotClient
from .http import HTTPClient
from . import helpers
from .errors import *

__version__ = "1.0"

VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel serial')

version_info = VersionInfo(major=1, minor=0, micro=0, releaselevel='final', serial=0)
