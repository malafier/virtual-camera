import pygame as pg
from config import *


class Camera:
    SHIFT_QUANTUM = 10
    R_QUANTUM = 1  # == PI/6

    def __init__(self):
        self.x, self.y, self.z = 0, 0, 0
        self.rot_x, self.rot_y, self.rot_z = 0, 0, 0
        self.vp_distance = 20
        self.fov_h = 90
        self.fov_v = self.fov_h * (W_HEIGHT / W_WIDTH)
        self.near_plane = 1
        self.far_plane = 1000

    def move(self, event_key):
        if event_key == pg.K_LEFT:
            self.x -= self.SHIFT_QUANTUM
        elif event_key == pg.K_RIGHT:
            self.x += self.SHIFT_QUANTUM
        elif event_key == pg.K_UP:
            self.y -= self.SHIFT_QUANTUM
        elif event_key == pg.K_DOWN:
            self.y += self.SHIFT_QUANTUM
        elif event_key == pg.K_w:
            self.z -= self.SHIFT_QUANTUM
        elif event_key == pg.K_s:
            self.z += self.SHIFT_QUANTUM
        elif event_key == pg.K_a:
            self.rot_y = (self.rot_y - self.R_QUANTUM) % 12
        elif event_key == pg.K_d:
            self.rot_y = (self.rot_y + self.R_QUANTUM) % 12
        elif event_key == pg.K_q:
            self.rot_x = (self.rot_x - self.R_QUANTUM) % 12
        elif event_key == pg.K_e:
            self.rot_x = (self.rot_x + self.R_QUANTUM) % 12
        elif event_key == pg.K_z:
            self.rot_z = (self.rot_z - self.R_QUANTUM) % 12
        elif event_key == pg.K_x:
            self.rot_z = (self.rot_z + self.R_QUANTUM) % 12

    def __str__(self):
        return f"Camera: ({self.x}, {self.y}, {self.z}), ({self.rot_x}, {self.rot_y}, {self.rot_z}), {self.vp_distance}"
