import numpy as np
from typing import List


def arr_to_rgb(arr: list) -> tuple:
    pivot = len(arr) // 2
    r = (int(sum(arr[:pivot])) * 150) % 256
    g = (int(arr[pivot]) * 150) % 256
    b = (int(sum(arr[pivot + 1:])) * 150) % 256
    return r, g, b


class Polygon:
    def __init__(self, face, vertices):
        self.rgb = arr_to_rgb(face)
        self.vertices = np.array(vertices)

    def plane_normal(self):
        v1 = self.vertices[0, :3]
        v2 = self.vertices[1, :3]
        v3 = self.vertices[2, :3]
        return np.cross(v2 - v1, v3 - v1)


def point_in_front_of_plane(point_plane: Polygon, i, normal_plane: Polygon) -> bool:
    normal = normal_plane.plane_normal()
    # print(normal, point_plane.vertices[i], normal_plane.vertices[0])
    vec = point_plane.vertices[i, :3] - normal_plane.vertices[0, :3]
    return np.dot(normal, vec) >= 0.0


def obscures(p: Polygon, q: Polygon) -> bool:
    # Extreme screen values of x of two faces do not overlap
    self_x_min, self_x_max = np.min(p.vertices[:, 0]), np.max(p.vertices[:, 0])
    other_x_min, other_x_max = np.min(q.vertices[:, 0]), np.max(q.vertices[:, 0])
    if self_x_min > other_x_max or self_x_max < other_x_min:
        return False

    # Extreme screen values of y of two faces do not overlap
    self_y_min, self_y_max = np.min(p.vertices[:, 1]), np.max(p.vertices[:, 1])
    other_y_min, other_y_max = np.min(q.vertices[:, 1]), np.max(q.vertices[:, 1])
    if self_y_min > other_y_max or self_y_max < other_y_min:
        return False

    # P is contained wholly in the back half-space of Q
    all_in_back = True
    for i in range(len(p.vertices)):
        if point_in_front_of_plane(p, i, q):
            all_in_back = False
    if not all_in_back:
        return False

    # Q is contained wholly in the front half-space of P
    all_in_front = True
    for i in range(len(q.vertices)):
        if not point_in_front_of_plane(q, i, p):
            all_in_front = False
    if not all_in_front:
        return False

    return True


def sort_by_z(polygons):
    return sorted(polygons, key=lambda x: np.mean(x.vertices[:, 2]), reverse=True)


def painter_algorithm(polygons: List[Polygon]):
    sorted_polygons = sort_by_z(polygons)
    draw_stack = []

    for polygon in sorted_polygons:
        # Check if the polygon is visible
        visible = True
        for other_polygon in draw_stack:
            if obscures(polygon, other_polygon):
                i = draw_stack.index(other_polygon)
                draw_stack = draw_stack[:i] + [polygon] + draw_stack[i:]
                visible = False
                break
        if visible:
            draw_stack.append(polygon)

    return draw_stack
