from enum import Enum, auto


class TopoNodeStatus(Enum):
    UNAVAILABLE = auto()
    AVAILABLE = auto()
    RUNNING = auto()
