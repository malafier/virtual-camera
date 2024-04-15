import os

import pygame as pg

from camera import Camera
from config import *
from scene import Scene

# Set up the window
window = pg.display.set_mode((W_WIDTH, W_HEIGHT), pg.RESIZABLE)
pg.display.set_caption("Virtual Camera")
os.environ["SDL_VIDEODRIVER"] = "x11"
pg.init()

if __name__ == "__main__":
    scene = Scene()
    camera = Camera()
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                camera.move(event.key)
                print(camera)

            scene.draw(window, camera)
    pg.quit()
