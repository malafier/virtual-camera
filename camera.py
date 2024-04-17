import pygame as pg
from config import *


class Camera:
    SHIFT_QUANTUM = 10
    R_QUANTUM = 1  # == PI/6

    def __init__(self):
        self.x, self.y, self.z = 0, 0, 0
        self.rot_x, self.rot_y, self.rot_z = 0, 0, 0
        self.vp_distance = 40

        # self.far_plane = 500
        self.vp_top = 20
        self.vp_bottom = -self.vp_top
        self.vp_right = self.vp_top * W_WIDTH / W_HEIGHT
        self.vp_left = -self.vp_right

    def move(self, event_key):
        if event_key == pg.K_LEFT:
            self.x -= self.SHIFT_QUANTUM
        elif event_key == pg.K_RIGHT:
            self.x += self.SHIFT_QUANTUM
        elif event_key == pg.K_UP:
            if pg.key.get_mods() & pg.KMOD_SHIFT:
                self.z -= self.SHIFT_QUANTUM
            else:
                self.y -= self.SHIFT_QUANTUM
        elif event_key == pg.K_DOWN:
            if pg.key.get_mods() & pg.KMOD_SHIFT:
                self.z += self.SHIFT_QUANTUM
            else:
                self.y += self.SHIFT_QUANTUM

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
                self.vp_distance += 10
            else:
                self.vp_distance = max(10, self.vp_distance - 10)

    def __str__(self):
        return f"Camera: ({self.x}, {self.y}, {self.z}), ({self.rot_x}, {self.rot_y}, {self.rot_z}), {self.vp_distance}"
