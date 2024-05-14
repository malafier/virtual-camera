import pygame as pg
import numpy as np

from rendering.camera import Camera
from rendering.projection import Projection
from rendering.transformations import *
from rendering.zbuffer import Polygon, pixel_color
from rendering.config import W_WIDTH, W_HEIGHT


class Scene:
    def __init__(self, camera: Camera):
        self.vertices, self.faces = [], []
        self.load_from_file("data/nodes.txt")
        self.camera: Camera = camera
        self.triangulate()

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

    def triangulate(self):
        new_faces = []
        for face in self.faces:
            if len(face) > 3:
                for i in range(1, len(face) - 1):
                    new_faces.append([face[0], face[i], face[i + 1]])
            else:
                new_faces.append(face)
        self.faces = new_faces

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
        y_min, y_max = max(y_min, 0), min(y_max, W_HEIGHT - 1)
        x_min, x_max = int(np.floor(np.min(vertices[:, 0]))), int(np.ceil(np.max(vertices[:, 0])))
        x_min, x_max = max(x_min, 0), min(x_max, W_WIDTH - 1)
        for i in range(x_min, x_max + 1):
            for j in range(y_min, y_max + 1):
                pg.draw.circle(window, pixel_color(i, j, polygons), (i, j), 1)
        pg.display.update()
