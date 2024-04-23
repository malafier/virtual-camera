import pygame as pg

from rendering.transformations import *

SHIFT_QUANTUM = 5
R_QUANTUM = 1  # == PI/6


class Camera:
    def __init__(self):
        self.position = 5, 5, -5, 1
        self.rot_x, self.rot_y, self.rot_z = 0, 0, 0
        self.forward = np.array([0, 0, 1, 1])
        self.up = np.array([0, 1, 0, 1])
        self.right = np.array([1, 0, 0, 1])

        self.vp_top = 1.0
        self.near_plane = 0.1

    def move(self, event_key):
        if event_key == pg.K_LEFT:
            self.position -= self.right * SHIFT_QUANTUM
        elif event_key == pg.K_RIGHT:
            self.position += self.right * SHIFT_QUANTUM
        elif event_key == pg.K_UP:
            if pg.key.get_mods() & pg.KMOD_SHIFT:
                self.position += self.up * SHIFT_QUANTUM
            else:
                self.position += self.forward * SHIFT_QUANTUM
        elif event_key == pg.K_DOWN:
            if pg.key.get_mods() & pg.KMOD_SHIFT:
                self.position -= self.up * SHIFT_QUANTUM
            else:
                self.position -= self.forward * SHIFT_QUANTUM

        elif event_key == pg.K_a:
            self.rot_y = (self.rot_y - R_QUANTUM) % 12
        elif event_key == pg.K_d:
            self.rot_y = (self.rot_y + R_QUANTUM) % 12
        elif event_key == pg.K_w:
            self.rot_x = (self.rot_x - R_QUANTUM) % 12
        elif event_key == pg.K_s:
            self.rot_x = (self.rot_x + R_QUANTUM) % 12
        elif event_key == pg.K_q:
            self.rot_z = (self.rot_z - R_QUANTUM) % 12
        elif event_key == pg.K_e:
            self.rot_z = (self.rot_z + R_QUANTUM) % 12

        elif event_key == pg.K_z:
            if pg.key.get_mods() & pg.KMOD_SHIFT:
                self.vp_top = min(3.0, round(10 * (self.vp_top + 0.2)) / 10)
            else:
                self.vp_top = max(0.2, round(10 * (self.vp_top - 0.2)) / 10)

    def matrix(self):
        cam_translation = translation(-self.position[0], -self.position[1], -self.position[2])

        rotation = rotation_x(self.rot_x) @ rotation_y(self.rot_y) @ rotation_z(self.rot_z)
        self.forward = np.array([0, 0, 1, 1]) @ rotation
        self.up = np.array([0, 1, 0, 1]) @ rotation
        self.right = np.array([1, 0, 0, 1]) @ rotation

        rx, ry, rz, _ = self.right
        ux, uy, uz, _ = self.up
        fx, fy, fz, _ = self.forward
        cam_rotation = np.array([
            [rx, ux, fx, 0],
            [ry, uy, fy, 0],
            [rz, uz, fz, 0],
            [0, 0, 0, 1]
        ])

        return cam_translation @ cam_rotation

    def __str__(self):
        return f"Camera: {self.position[:3]}, ({self.rot_x}, {self.rot_y}, {self.rot_z}), {self.vp_top}"
