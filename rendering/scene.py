import pygame as pg

from rendering.camera import Camera
from rendering.painter import painter_algorithm, Polygon
from rendering.projection import Projection
from rendering.transformations import *


class Scene:
    def __init__(self, camera: Camera):
        self.vertices, self.faces = [], []
        self.load_from_file("data/planes.txt")
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

        polygons = []
        for face in self.faces:
            polygons.append(Polygon(face, vertices[face]))
        polygons = painter_algorithm(polygons)

        for poly in polygons:
            polygon = np.array(poly.vertices)
            polygon = polygon @ projection.projection_matrix
            polygon[:, -1] = np.where(polygon[:, -1] == 0, 1, polygon[:, -1])
            polygon /= polygon[:, -1].reshape(-1, 1)
            polygon = polygon @ projection.scaling_matrix
            polygon = polygon[:, :2]

            pg.draw.polygon(window, poly.rgb, polygon)
        pg.display.update()
