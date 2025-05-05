# vehicles/car.py

import pygame
import math

CELL_SIZE = 100
CAR_WIDTH = 10
CAR_LENGTH = 20
QUEUE_GAP = 10  # Minimum pixel gap between cars

class Car:
    def __init__(self, path, speed=2):
        self.path = path
        self.speed = speed
        self.index = 0
        self.t = 0.0

    def update(self, city=None, cars=None, pixel_coords_func=None):
        if self.index >= len(self.path) - 1:
            return  # Arrived

        current_node = self.path[self.index]
        next_node = self.path[self.index + 1]

        if self.t == 0.0 and city:
            if city.intersections[current_node].has_light and not city.intersections[current_node].is_green:
                return  # Stop at red light

        # Queuing behavior
        if cars and pixel_coords_func:
            my_pos = self.get_position(pixel_coords_func)
            for lead in cars:
                if lead is self:
                    continue
                if lead.index == self.index + 1:
                    lead_pos = lead.get_position(pixel_coords_func)
                    dist = math.hypot(my_pos[0] - lead_pos[0], my_pos[1] - lead_pos[1])
                    if dist < CAR_LENGTH + QUEUE_GAP:
                        return  # Too close to car ahead

        # Move toward the next node
        self.t += self.speed * 0.02
        if self.t >= 1.0:
            self.t = 0.0
            self.index += 1

    def get_position(self, pixel_coords_func):
        if self.index >= len(self.path) - 1:
            return pixel_coords_func(self.path[-1])

        p1 = pixel_coords_func(self.path[self.index])
        p2 = pixel_coords_func(self.path[self.index + 1])

        x = p1[0] + (p2[0] - p1[0]) * self.t
        y = p1[1] + (p2[1] - p1[1]) * self.t
        return (x, y)
