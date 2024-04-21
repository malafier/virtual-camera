import pygame as pg

from rendering.camera import Camera
from rendering.projection import Projection
from rendering.transformations import *


class Scene:
    def __init__(self, camera: Camera):
        self.vertices, self.edges = [], []
        self.load_from_file("data/nodes.txt")
        self.camera: Camera = camera

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

    def draw(self, window):
        window.fill(Colour.BLACK.value)
        projection = Projection(self.camera)

        vertices = self.vertices @ self.camera.matrix()
        vertices = vertices @ projection.projection_matrix
        vertices /= vertices[:, -1].reshape(-1, 1)
        # vertices[(vertices > 2) | (vertices < -2)] = 0
        vertices = vertices @ projection.scaling_matrix
        vertices = vertices[:, :2]

        for edge in self.edges:
            if np.any(edge == H_WIDTH) or np.any(edge == H_HEIGHT):
                continue
            pg.draw.line(window, Colour.WHITE.value, vertices[edge[0]], vertices[edge[1]])
        for vertex in vertices:
            if np.any(vertex == W_WIDTH) or np.any(vertex == W_HEIGHT):
                continue
            pg.draw.circle(window, Colour.RED.value, vertex, 4)
        pg.display.update()
