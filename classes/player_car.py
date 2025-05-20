import time
import os
import pygame as pg
from settings import *

ROAD_WIDTH = 300
LANE_WIDTH = ROAD_WIDTH // 3
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
RED = (200, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

class PlayerCar:
    def __init__(self, screen_width, screen_height):
        self.width = 200
        self.height = 100
        self.color = BLUE

        self.lane_index = 2
        self.speed = 0.0
        self.max_speed = 8
        self.acceleration = 0.1
        self.deceleration = 0.2
        self.friction = 0.05

        #self.x = (screen_width - self.width) // 2
        self.y = screen_height / 2 + self.height / 2

        self.lane_positions = {
            1: (screen_width - ROAD_WIDTH) // 2 + (LANE_WIDTH // 2) - (self.width // 2),  # Lane 1 (left)
            2: (screen_width - ROAD_WIDTH) // 2 + LANE_WIDTH + (LANE_WIDTH // 2) - (self.width // 2),  # Lane 2 (middle)
            3: (screen_width - ROAD_WIDTH) // 2 + 2 * LANE_WIDTH + (LANE_WIDTH // 2) - (self.width // 2)  # Lane 3 (right)
        }
        self.x = self.lane_positions[self.lane_index]  # Start in the middle lane (lane 2)
        self.target_x = self.x
        self.lane_switch_speed = 4  # Speed at which the car switches lanes
        self.last_lane_switch_time = 0  # Track the last time a lane switch occurred
        self.lane_switch_cooldown = 0.2  # Cooldown in seconds

        # Load the car image
        try:
            self.image = pg.image.load(os.path.join('assets', 'player_car.png')).convert_alpha()
            # Scale the image to match car dimensions
            self.image = pg.transform.scale(self.image, (self.width, self.height))
        except pg.error as e:
            print(f"Couldn't load car image: {e}")
            # Fallback to rectangle if image loading fails
            self.image = None

    def update(self):
        self.movement()

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            # Fallback to original rectangle if image failed to load
            #print(f"Couldn't draw car image")
            pg.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def movement(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.speed += self.acceleration
            if self.speed > self.max_speed:
                self.speed = self.max_speed
        elif keys[pg.K_s]:  # Decelerate
            self.speed -= self.deceleration
            if self.speed < -2:
                self.speed = -2

    def move(self, keys):
        # Handle acceleration and deceleration
        if keys[pg.K_w]:  # Accelerate
            self.speed += self.acceleration
            if self.speed > self.max_speed:
                self.speed = self.max_speed
        elif keys[pg.K_s]:  # Decelerate
            self.speed -= self.deceleration
            if self.speed < -2:
                self.speed = -2
        else:  # Apply friction
            if self.speed > 0:
                self.speed -= self.friction
                if self.speed < 0:
                    self.speed = 0
            elif self.speed < 0:
                self.speed += self.friction
                if self.speed > 0:
                    self.speed = 0

        # Move the car vertically based on speed
        self.y -= self.speed

        # Prevent the car from moving too high (optional)
        if self.y < 100:
            self.y = 100

        # Smoothly move the car to the target lane
        if self.x < self.target_x:
            self.x += self.lane_switch_speed
            if self.x > self.target_x:  # Prevent overshooting
                self.x = self.target_x
        elif self.x > self.target_x:
            self.x -= self.lane_switch_speed
            if self.x < self.target_x:  # Prevent overshooting
                self.x = self.target_x

    def handle_lane_switch(self, event):
        current_time = time.time()
        if current_time - self.last_lane_switch_time > self.lane_switch_cooldown:
            if event.key == pg.K_a and self.lane_index > 1:  # Move left (from lane 3 to 2, or lane 2 to 1)
                self.lane_index -= 1
                self.target_x = self.lane_positions[self.lane_index]
                self.last_lane_switch_time = current_time

            if event.key == pg.K_d and self.lane_index < 3:  # Move right (from lane 1 to 2, or lane 2 to 3)
                self.lane_index += 1
                self.target_x = self.lane_positions[self.lane_index]
                self.last_lane_switch_time = current_time