from enum import Enum

from numpy import pi


class Colour(Enum):
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)
    BLACK = (20, 20, 20)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)


ROTATION_QUANTUM = pi / 6

W_HEIGHT = 720
W_WIDTH = 1280
H_HEIGHT = W_HEIGHT // 2
H_WIDTH = W_WIDTH // 2
