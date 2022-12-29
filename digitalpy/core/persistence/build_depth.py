from enum import Enum

class BuildDepth(Enum):
    INFINITE = -1
    SINGLE = -2
    REQUIRED = -4
    PROXIES_ONLY = -8
    MAX = 10 