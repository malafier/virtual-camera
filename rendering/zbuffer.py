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
    def inside_polygon(self, x, y):
        crossings = 0
        for i in range(len(self.vertices)):
            x1, y1, _, _ = self.vertices[i]
            x2, y2, _, _ = self.vertices[(i + 1) % len(self.vertices)]
            if (y1 > y) != (y2 > y) and x < ((x2 - x1) * (y - y1) / (y2 - y1) + x1):
                crossings += 1
        return crossings % 2 == 1

    @jit(nopython=True)
    def depth_interpolation(self, x, y):
        x0, y0, z0, _ = self.vertices[0]
        x1, y1, z1, _ = self.vertices[1]
        x2, y2, z2, _ = self.vertices[2]

        total_area = 0.5 * ((y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2))
        w0 = 0.5 * ((y1 - y2) * (x - x2) + (x2 - x1) * (y - y2)) / total_area
        w1 = 0.5 * ((y2 - y0) * (x - x2) + (x0 - x2) * (y - y2)) / total_area
        w2 = 1 - w0 - w1

        return w0 * z0 + w1 * z1 + w2 * z2


def pixel_color(x, y, polygons):
    deepest = float("inf")
    color = Colour.BLACK.value
    for polygon in polygons:
        if polygon.inside_polygon(x, y):
            depth = polygon.depth_interpolation(x, y)
            if depth < deepest:
                deepest = depth
                color = polygon.rgb
    return color
