from enum import Enum


class ANPRState(Enum):

    WAITING = 1

    COLLECTING = 2

    PROCESSING = 3

    COOLDOWN = 4