
from enum import Enum

class ClientStatus(Enum):
    CONNECTING = "CONNECTING"
    CONNECTED = "CONNECTED"
    DISCONNECTED = "DISCONNECTED"
    TERMINATED = "TERMINATED"

