import pygame as pg
import numpy as np
from camera import Camera
from config import *
from transformations import *


def project(point, cam: Camera):
    # projected = point @ np.array([
    #     [(cam.vp_right-cam.vp_left)/(2*cam.vp_distance), 0, 0, (cam.vp_right+cam.vp_left)/(2*cam.vp_distance)],
    #     [0, (cam.vp_top-cam.vp_bottom)/(2*cam.vp_distance), 0, (cam.vp_top+cam.vp_bottom)/(2*cam.vp_distance)],
    #     [0, 0, 0, -1],
    #     [0, 0, (-cam.far_plane+cam.vp_distance)/(2*cam.far_plane*cam.vp_distance), (-cam.far_plane+cam.vp_distance)/(2*cam.vp_distance)]
    # ])
    # projected /= projected[0, 3] if projected[0, 3] != 0 else 1
    # projected = np.array([
    #     [cam.vp_distance/cam.vp_right, 0, 0, 0],
    #     [0, cam.vp_distance/cam.vp_top, 0, 0],
    #     [0, 0, -1, -2 * cam.vp_distance],
    #     [0, 0, -1, 0]
    # ]) @ point.T
    projected = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 1/cam.vp_distance, 0]
    ]) @ point.T
    projected = projected.T
    # projected /= projected[:, -1].reshape(-1, 1) if projected[:, -1].any() else 1
    # projected[(projected < -1) | (projected > 1)] = 0
    projected /= projected[0, 3] if projected[0, 3] != 0 else 1
    return projected


def scale_to_screen(point):
    return point[0, 0] + W_WIDTH // 2, -point[0, 1] + W_HEIGHT // 2


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

                if line.startswith("e "):
                    self.edges.append(tuple(map(int, line.strip().split()[1:])))
            self.vertices = np.array(vertices)

    def draw(self, window, camera: Camera):
        window.fill(Colour.BLACK.value)

        debug = True  # TODO: remove later
        for edge in self.edges:
            node1 = np.matrix(self.vertices[edge[0]])
            node2 = np.matrix(self.vertices[edge[1]])

            # translation and rotation
            if debug:
                print(node1, node2)
            node1 = translate(node1, camera.x, camera.y, camera.z)
            node2 = translate(node2, camera.x, camera.y, camera.z)
            if debug:
                print("t: ", node1, node2)
            node1 = rotate_x(node1, camera.rot_x)
            node2 = rotate_x(node2, camera.rot_x)
            node1 = rotate_y(node1, camera.rot_y)
            node2 = rotate_y(node2, camera.rot_y)
            node1 = rotate_z(node1, camera.rot_z)
            node2 = rotate_z(node2, camera.rot_z)
            if debug:
                print("r: ", node1, node2)

            # projection
            node1 = project(node1, camera)
            node2 = project(node2, camera)
            if debug:
                print("p: ", node1, node2)
            point1 = scale_to_screen(node1)
            point2 = scale_to_screen(node2)
            if debug:
                print("s: ", point1, point2)
            debug = False  # TODO: remove later

            # drawing
            pg.draw.line(window, Colour.WHITE.value, (int(point1[0]), int(point1[1])), (int(point2[0]), int(point2[1])))
            pg.draw.circle(window, Colour.BLUE.value, (int(point1[0]), int(point1[1])), 4)
            pg.draw.circle(window, Colour.BLUE.value, (int(point2[0]), int(point2[1])), 4)
        pg.display.update()
