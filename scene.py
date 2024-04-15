import pygame as pg
import numpy as np
from camera import Camera
from config import *


def translate(point, dx, dy, dz):
    return point @ np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [dx, dy, dz, 1]
    ])


def rotate_x(point, angle):
    angle *= ROTATION_QUANTUM
    return point @ np.array([
        [1, 0, 0, 0],
        [0, np.cos(angle), np.sin(angle), 0],
        [0, -np.sin(angle), np.cos(angle), 0],
        [0, 0, 0, 1]
    ])


def rotate_y(point, angle):
    angle *= ROTATION_QUANTUM
    return point @ np.array([
        [np.cos(angle), 0, -np.sin(angle), 0],
        [0, 1, 0, 0],
        [np.sin(angle), 0, np.cos(angle), 0],
        [0, 0, 0, 1]
    ])


def rotate_z(point, angle):
    angle *= ROTATION_QUANTUM
    return point @ np.array([
        [np.cos(angle), np.sin(angle), 0, 0],
        [-np.sin(angle), np.cos(angle), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])


def project(point, distance):
    projected = point @ np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 1 / distance],
        [0, 0, 0, 0]
    ])
    projected /= projected[0, 3] if projected[0, 3] != 0 else 1
    return projected


def to_screen(point, width, height):
    return point[0, 0] + width // 2, -point[0, 1] + height // 2


class Scene:
    def __init__(self):
        self.vertices = None
        self.edges = []
        self.load_from_file("nodes.txt")

    def load_from_file(self, filename):
        with open(filename, "r") as f:
            vertices = []
            for line in f:
                if line.startswith("v "):
                    vertices.append(tuple(map(float, line.strip().split()[1:])))
                    vertices[-1] = vertices[-1][0], vertices[-1][1], vertices[-1][2], 1.0
                self.vertices = np.matrix(vertices)

                if line.startswith("e "):
                    self.edges.append(tuple(map(int, line.strip().split()[1:])))

        print(self.vertices)
        # print(self.edges)

    def draw(self, window, camera: Camera):
        window.fill(Colour.BLACK.value)

        for edge in self.edges:
            node1 = np.matrix(self.vertices[edge[0]])
            node2 = np.matrix(self.vertices[edge[1]])

            # translation and rotation
            node1 = translate(node1, -camera.x, -camera.y, -camera.z)
            node2 = translate(node2, -camera.x, -camera.y, -camera.z)
            # node1 = rotate_x(node1, camera.rot_x)
            # node2 = rotate_x(node2, camera.rot_x)
            # node1 = rotate_y(node1, camera.rot_y)
            # node2 = rotate_y(node2, camera.rot_y)
            # node1 = rotate_z(node1, camera.rot_z)
            # node2 = rotate_z(node2, camera.rot_z)

            # projection
            node1 = project(node1, camera.vp_distance)
            node2 = project(node2, camera.vp_distance)
            point1 = to_screen(node1, W_WIDTH, W_HEIGHT)
            point2 = to_screen(node2, W_WIDTH, W_HEIGHT)

            # drawing
            pg.draw.line(window, Colour.WHITE.value, (int(point1[0]), int(point1[1])), (int(point2[0]), int(point2[1])))
            pg.draw.circle(window, Colour.BLUE.value, (int(point1[0]), int(point1[1])), 4)
            pg.draw.circle(window, Colour.BLUE.value, (int(point2[0]), int(point2[1])), 4)

        pg.display.update()
