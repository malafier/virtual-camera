import numpy as np

from rendering.config import *


class Projection:
    def __init__(self, cam):
        near = cam.near_plane
        far = near * 1000

        top = cam.vp_top
        bottom = -top
        right = top * W_WIDTH / W_HEIGHT
        left = -right

        self.projection_matrix = np.array([
            [2 / (right - left), 0, 0, 0],
            [0, 2 / (top - bottom), 0, 0],
            [0, 0, (far + near) / (near - far), 1],
            [0, 0, -2 * far * near / (far - near), 0]
        ])

        self.scaling_matrix = np.array([
            [H_WIDTH, 0, 0, 0],
            [0, -H_HEIGHT, 0, 0],
            [0, 0, 1, 0],
            [H_WIDTH, H_HEIGHT, 0, 1]
        ])
