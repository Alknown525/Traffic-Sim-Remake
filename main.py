import pygame as pg
import sys
from settings import WIN_RES
from mode7 import Mode7
from classes.start_screen import StartScreen
from classes.player_car import PlayerCar


class App:
    def __init__(self):
        self.screen = pg.display.set_mode(WIN_RES)
        self.clock = pg.time.Clock()
        self.mode7 = Mode7(self)
        self.player_car = PlayerCar(WIN_RES[0], WIN_RES[1])

    def update(self):
        self.mode7.update()
        self.player_car.update()
        self.clock.tick()
        pg.display.set_caption(f"FPS: {self.clock.get_fps() : .1f}")

    def draw(self):
        self.mode7.draw()
        self.player_car.draw(self.screen)
        pg.display.flip()

    def get_time(self):
        self.time = pg.time.get_ticks() / 1000.0

    def check_event(self):
        for i in pg.event.get():
            if i.type == pg.QUIT or (i.type == pg.KEYDOWN and i.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            if i.type == pg.KEYDOWN:  # Handle lane switching
                self.player_car.handle_lane_switch(i)

    def run(self):
        while True:
            self.check_event()
            self.get_time()
            self.update()
            self.draw()

if __name__ == '__main__':
    app = App()
    app.run()