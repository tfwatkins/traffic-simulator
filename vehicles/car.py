# vehicles/car.py

import pygame
from utils.pathfinder import dijkstra_path

CELL_SIZE = 100
CAR_COLOR = (255, 100, 100)
CAR_WIDTH = 10
CAR_LENGTH = 20
AVOID_RADIUS = 50  # pixels ahead to check for other cars

class Car:
    def __init__(self, path, speed=2):
        self.path = path
        self.speed = speed
        self.index = 0
        self.t = 0.0
        self.retries = 0

    def update(self, city=None, cars=None, pixel_coords_func=None, quadtree=None):
        if self.index >= len(self.path) - 1:
            return  # Reached destination

        current_node = self.path[self.index]
        next_node = self.path[self.index + 1]

        # Only check light when starting to move to next segment
        if self.t == 0.0 and city:
            intersection = city.intersections[current_node]
            if intersection.has_light and not intersection.is_green:
                return  # Stop at red light

            # Check for car ahead
            if quadtree and self._is_blocked(quadtree, current_node, next_node, pixel_coords_func):
                self.retries += 1
                if self.retries < 3:
                    return  # wait and retry
                else:
                    self._reroute(city)
                    return
            else:
                self.retries = 0

        # Move forward toward the next node
        self.t += self.speed * 0.02
        if self.t >= 1.0:
            self.t = 0.0
            self.index += 1  # Proceed to next segment

    def _is_blocked(self, quadtree, current_node, next_node, pixel_coords_func):
        # Get target position
        p1 = pixel_coords_func(current_node)
        p2 = pixel_coords_func(next_node)
        mid_x = p1[0] + (p2[0] - p1[0]) * 0.5
        mid_y = p1[1] + (p2[1] - p1[1]) * 0.5

        neighbors = quadtree.query_range((mid_x, mid_y, AVOID_RADIUS, AVOID_RADIUS))
        return any(car != self for car in neighbors)

    def _reroute(self, city):
        start = self.path[self.index]
        end = self.path[-1]
        new_path = dijkstra_path(city, start, end)
        if new_path:
            self.path = new_path
            self.index = 0
            self.t = 0.0

    def get_position(self, pixel_coords_func):
        if self.index >= len(self.path) - 1:
            return pixel_coords_func(self.path[-1])

        p1 = pixel_coords_func(self.path[self.index])
        p2 = pixel_coords_func(self.path[self.index + 1])

        x = p1[0] + (p2[0] - p1[0]) * self.t
        y = p1[1] + (p2[1] - p1[1]) * self.t
        return (x, y)
