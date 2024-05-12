import numpy as np
import pygame as pg

from rendering.camera import Camera
from rendering.zbuffer import Polygon, pixel_color
from rendering.projection import Projection
from rendering.transformations import *


class Scene:
    def __init__(self, camera: Camera):
        self.vertices, self.faces = [], []
        self.load_from_file("data/nodes.txt")
        self.camera: Camera = camera

    def load_from_file(self, filename):
        with open(filename, "r") as f:
            vertices = []
            for line in f:
                if line.startswith("v "):
                    vertices.append(tuple(map(float, line.strip().split()[1:])))
                    vertices[-1] = vertices[-1][0], vertices[-1][1], vertices[-1][2], 1.0

                if line.startswith("f "):
                    self.faces.append(list(map(int, line.strip().split()[1:])))
        self.vertices = np.array(vertices)

    def draw(self, window):
        window.fill(Colour.BLACK.value)
        projection = Projection(self.camera)

        vertices = self.vertices @ self.camera.matrix()
        z_values = vertices[:, 2].copy()

        vertices = vertices @ projection.projection_matrix
        vertices[:, -1] = np.where(vertices[:, -1] == 0, 1, vertices[:, -1])
        vertices /= vertices[:, -1].reshape(-1, 1)
        vertices = vertices @ projection.scaling_matrix
        vertices[:, 2] = z_values

        polygons = []
        for face in self.faces:
            polygons.append(Polygon(face, vertices[face]))

        y_min, y_max = int(np.floor(np.min(vertices[:, 1]))), int(np.ceil(np.max(vertices[:, 1])))
        x_min, x_max = int(np.floor(np.min(vertices[:, 0]))), int(np.ceil(np.max(vertices[:, 0])))
        for i in range(x_min, x_max+1):
            for j in range(y_min, y_max+1):
                pg.draw.circle(window, pixel_color(i, j, polygons), (i, j), 1)
        pg.display.update()
