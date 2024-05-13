import numpy as np
from numba import jit

from rendering.config import Colour


def arr_to_rgb(arr: list) -> tuple:
    pivot = len(arr) // 2
    r = (int(sum(arr[:pivot])) * 170) % 256
    g = (int(arr[pivot]) * 170) % 256
    b = (int(sum(arr[pivot + 1:])) * 170) % 256
    return r, g, b


class Polygon:
    def __init__(self, face, vertices):
        self.rgb = arr_to_rgb(face)
        self.vertices = np.array(vertices)


@jit(nopython=True)
def inside_and_depth(x, y, triangle):
    x_min, x_max = np.min(triangle[:, 0]), np.max(triangle[:, 0])
    y_min, y_max = np.min(triangle[:, 1]), np.max(triangle[:, 1])
    if x < x_min or x > x_max or y < y_min or y > y_max:
        return False, -1

    x_0, y_0, z_0, _ = triangle[0]
    x_1, y_1, z_1, _ = triangle[1]
    x_2, y_2, z_2, _ = triangle[2]

    denominator = (y_1 - y_2) * (x_0 - x_2) + (x_2 - x_1) * (y_0 - y_2)
    if denominator == 0:
        return False, -1
    alpha = ((y_1 - y_2) * (x - x_2) + (x_2 - x_1) * (y - y_2)) / denominator
    beta = ((y_2 - y_0) * (x - x_2) + (x_0 - x_2) * (y - y_2)) / denominator
    gamma = 1 - alpha - beta

    is_inside = (0 <= alpha <= 1) and (0 <= beta <= 1) and (0 <= gamma <= 1)
    if not is_inside:
        return False, -1
    depth = alpha * z_0 + beta * z_1 + gamma * z_2
    return is_inside, depth


def pixel_color(x, y, polygons):
    deepest = float("inf")
    color = Colour.BLACK.value
    for polygon in polygons:
        is_inside, depth = inside_and_depth(x, y, polygon.vertices)
        if is_inside and depth < deepest:
            deepest = depth
            color = polygon.rgb
    return color
