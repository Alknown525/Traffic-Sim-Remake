import pygame as pg
import numpy as np
from settings import *
from numba import njit, prange

class Mode7:
    def __init__(self, app):
        self.app = app
        self.floor_tex = pg.image.load('textures/floor_2.png').convert()
        self.tex_size = self.floor_tex.get_size()
        self.floor_array = pg.surfarray.array3d(self.floor_tex)

        self.ceil_tex = pg.image.load('textures/ceil_2.png').convert()
        self.ceil_tex = pg.transform.scale(self.ceil_tex, self.tex_size)
        self.ceil_array = pg.surfarray.array3d(self.ceil_tex)

        self.screen_array = pg.surfarray.array3d(pg.Surface(WIN_RES))

        self.alt = 1.0
        self.angle = 0.0
        self.pos = np.array([0.0, 0.0])

        self.current_speed = 0.0
        self.min_speed = 0.0
        self.max_speed = 5.0 * SPEED
        self.acceleration = 0.01 * SPEED
        self.deceleration = 0.03 * SPEED

    def update(self):
        self.movement()
        self.screen_array = self.render_frame(self.floor_array, self.ceil_array, self.screen_array,
                                              self.tex_size, self.angle, self.pos, self.alt)

    def draw(self):
        pg.surfarray.blit_array(self.app.screen, self.screen_array)

    @staticmethod
    @njit(fastmath=True, parallel=True)
    def render_frame(floor_array, ceil_array, screen_array, tex_size, angle, player_pos, alt):

        sin, cos = np.sin(angle), np.cos(angle)
        

        # iterating over the screen array
        for i in prange(WIDTH):
            new_alt = alt
            for j in range(HORIZON_HEIGHT, HEIGHT):
                x = HALF_WIDTH - i
                y = (j - HORIZON_HEIGHT) + FOCAL_LEN
                z = j - HORIZON_HEIGHT + new_alt

                # rotation
                px = (x * cos - y * sin)
                py = (x * sin + y * cos)

                # floor projection and transformation
                floor_x = px / z - player_pos[1]
                floor_y = py / z + player_pos[0]

                # floor pos and color
                floor_pos = int(floor_x * SCALE % tex_size[0]), int(floor_y * SCALE % tex_size[1])
                floor_col = floor_array[floor_pos]

                # ceil projection and transformation
                ceil_x = alt * px / z - player_pos[1] * 0.3
                ceil_y = alt * py / z + player_pos[0] * 0.3

                # ceil pos and color
                ceil_pos = int(ceil_x * SCALE % tex_size[0]), int(ceil_y * SCALE % tex_size[1])
                ceil_col = ceil_array[ceil_pos]

                # shading
                # depth = 4 * abs(z) / HALF_HEIGHT
                depth = min(max(2.5 * (abs(z) / HALF_HEIGHT), 0), 1)
                fog = (1 - depth) * 230

                floor_col = (floor_col[0] * depth + fog,
                             floor_col[1] * depth + fog,
                             floor_col[2] * depth + fog)

                ceil_col = (ceil_col[0] * depth + fog,
                            ceil_col[1] * depth + fog,
                            ceil_col[2] * depth + fog)

                # fill screen array
                screen_array[i, j] = floor_col
                #screen_array[i, HORIZON_HEIGHT - (j - HORIZON_HEIGHT)] = ceil_col
                screen_array[i, HORIZON_HEIGHT + (-j + HORIZON_HEIGHT)] = ceil_col
                #if j < HEIGHT // 4:
                #    screen_array[i, j] = ceil_col

                # next depth
                new_alt += alt

        return screen_array

    # this is movement of the camera, not the player, need player movement
    def movement(self):
        sin_a = np.sin(self.angle)
        cos_a = np.cos(self.angle)

        
        # Handle speed changes
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.current_speed = min(self.current_speed + self.acceleration, self.max_speed)
        elif keys[pg.K_s]:
            self.current_speed = max(self.current_speed - self.deceleration, self.min_speed)
        else:
            # Gradually slow down when no key is pressed
            if self.current_speed > 0:
                self.current_speed = max(self.current_speed - self.deceleration * 0.1, 0)
        
        # Apply constant forward motion based on current_speed
        dx = self.current_speed * cos_a
        dy = self.current_speed * sin_a
        
        # Lateral movement (optional - you can keep or remove)
        if keys[pg.K_a]:
            dx += SPEED * sin_a
            dy += -SPEED * cos_a
        if keys[pg.K_d]:
            dx += -SPEED * sin_a
            dy += SPEED * cos_a

        self.pos[0] += dx
        self.pos[1] += dy

        if keys[pg.K_LEFT]:
            self.angle -= SPEED
        if keys[pg.K_RIGHT]:
            self.angle += SPEED

        if keys[pg.K_DOWN]:
            self.alt += SPEED
        if keys[pg.K_UP]:
            self.alt -= SPEED
        self.alt = min(max(self.alt, 0.1), 10.0)