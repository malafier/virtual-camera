import numpy as np
from typing import List


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

    def distance(self):
        centroid = np.mean(self.vertices[:, :3], axis=0)
        return np.sqrt(np.sum(centroid ** 2))

    def plane_normal(self):
        A = self.vertices[0, :3]
        B = self.vertices[1, :3]
        C = self.vertices[2, :3]
        normal = np.cross(B - A, C - A)
        print("n before: ", normal)
        if np.dot(normal, -A) < 0.0:
            normal = -normal
        print("n after: ", normal)
        return normal


# result > 0 means point is in front of the plane, result < 0 means point is behind the plane
def point_position_by_plane(point_plane: Polygon, i, normal_plane: Polygon) -> bool:
    normal = normal_plane.plane_normal()
    vec = point_plane.vertices[i, :3] - normal_plane.vertices[0, :3]
    print("vec: ", vec)
    return np.dot(normal, vec)


def p_obstructs_q(p: Polygon, q: Polygon) -> bool:
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
        print("P in back", i, ": ", point_position_by_plane(p, i, q))
        if not point_position_by_plane(p, i, q) < 0.0:
            all_in_back = False
            break
    if all_in_back:
        return False

    # Q is contained wholly in the front half-space of P
    all_in_front = True
    for i in range(len(q.vertices)):
        print("Q in front", i, ": ", point_position_by_plane(q, i, p))
        if not point_position_by_plane(q, i, p) > 0.0:
            all_in_front = False
            break
    if all_in_front:
        return False

    return True


def sort_by_distance(polygons):
    return sorted(polygons, key=lambda x: x.distance(), reverse=True)


def painter_algorithm(polygons: List[Polygon]):
    sorted_polygons = sort_by_distance(polygons)
    print("===============")
    print("Polygons: ")
    print(sorted_polygons[0].rgb, sorted_polygons[0].vertices)
    print(sorted_polygons[1].rgb, sorted_polygons[1].vertices)

    for i in range(len(sorted_polygons) - 1, 0, -1):
        j = i - 1
        while j >= 0 and p_obstructs_q(sorted_polygons[j], sorted_polygons[j+1]):
            sorted_polygons[j], sorted_polygons[j+1] = sorted_polygons[j+1], sorted_polygons[j]
            j -= 1
    print("Polygons: ")
    print(sorted_polygons[0].rgb, sorted_polygons[0].vertices)
    print(sorted_polygons[1].rgb, sorted_polygons[1].vertices)

    # for polygon in sorted_polygons:
    #     not_obstructed = True
    #     i = len(draw_order) - 1
    #     while i > 0 and p_obstructs_q(polygon, draw_order[i]):
    #         not_obstructed = False
    #         i -= 1

    #     if not_obstructed:
    #         draw_order.append(polygon)
    #     else:
    #         draw_order = draw_order[:i] + [polygon] + draw_order[i:]
    return sorted_polygons
