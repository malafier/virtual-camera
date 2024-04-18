import pygame as pg

from camera.transformations import *


class Camera:
    SHIFT_QUANTUM = 4
    R_QUANTUM = 1  # == PI/6

    def __init__(self):
        self.x, self.y, self.z = 0, -2, 10
        self.rot_x, self.rot_y, self.rot_z = -1, 0, 0

        self.near_plane = 0.1
        self.far_plane = self.near_plane * 1000
        self.vp_top = 1

    def move(self, event_key):
        if event_key == pg.K_LEFT:
            self.x += self.SHIFT_QUANTUM
        elif event_key == pg.K_RIGHT:
            self.x -= self.SHIFT_QUANTUM
        elif event_key == pg.K_UP:
            if pg.key.get_mods() & pg.KMOD_SHIFT:
                self.y -= self.SHIFT_QUANTUM
            else:
                self.z -= self.SHIFT_QUANTUM
        elif event_key == pg.K_DOWN:
            if pg.key.get_mods() & pg.KMOD_SHIFT:
                self.y += self.SHIFT_QUANTUM
            else:
                self.z += self.SHIFT_QUANTUM

        elif event_key == pg.K_a:
            self.rot_y = (self.rot_y - self.R_QUANTUM) % 12
        elif event_key == pg.K_d:
            self.rot_y = (self.rot_y + self.R_QUANTUM) % 12
        elif event_key == pg.K_w:
            self.rot_x = (self.rot_x - self.R_QUANTUM) % 12
        elif event_key == pg.K_s:
            self.rot_x = (self.rot_x + self.R_QUANTUM) % 12
        elif event_key == pg.K_q:
            self.rot_z = (self.rot_z - self.R_QUANTUM) % 12
        elif event_key == pg.K_e:
            self.rot_z = (self.rot_z + self.R_QUANTUM) % 12

        elif event_key == pg.K_z:
            if pg.key.get_mods() & pg.KMOD_SHIFT:
                self.vp_top = min(2.0, self.vp_top + 0.2)
            else:
                self.vp_top = max(0.4, self.vp_top - 0.2)

    def matrix(self):
        cam_translation = translation(self.x, self.y, self.z)

        rotation = rotation_x(self.rot_x) @ rotation_y(self.rot_y) @ rotation_z(self.rot_z)
        forward = np.array([0, 0, 1, 1]) @ rotation
        up = np.array([0, 1, 0, 1]) @ rotation
        right = np.array([1, 0, 0, 1]) @ rotation

        rx, ry, rz, _ = right
        ux, uy, uz, _ = up
        fx, fy, fz, _ = forward
        cam_rotation = np.array([
            [rx, ry, rz, 0],
            [ux, uy, uz, 0],
            [fx, fy, fz, 0],
            [0, 0, 0, 1]
        ])

        return cam_translation @ cam_rotation

    def __str__(self):
        return f"Camera: ({self.x}, {self.y}, {self.z}), ({self.rot_x}, {self.rot_y}, {self.rot_z}), {self.vp_top}"
