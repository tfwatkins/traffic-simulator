# utils/visualizer.py

import pygame

CELL_SIZE = 100
ROAD_WIDTH = 30
INTERSECTION_RADIUS = 10
CAR_WIDTH = 10
CAR_LENGTH = 20

class Visualizer:
    def __init__(self, city, width=800, height=800):
        pygame.init()
        self.city = city
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Urban Traffic Simulator")
        self.clock = pygame.time.Clock()

    def get_pixel_coords(self, node_name):
        x_str, y_str = node_name.split(",")
        x, y = int(x_str), int(y_str)
        return (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2)

    # def get_intersection_color(self, name):
    #     intersection = self.city.intersections[name]
    #     states = intersection.light_state.values()
    #     if "green" in states and sum(1 for s in states if s == "green") == 1:
    #         return (0, 255, 0)
    #     elif "green" in states:
    #         return (0, 255, 255)
    #     return (255, 0, 0)

    def get_intersection_color(self, name):
        intersection = self.city.intersections[name]
        return (0, 255, 0) if intersection.is_green else (255, 0, 0)



    def render(self, city, tick=None):
        self.screen.fill((30, 30, 30))  # Clear background

        # 1. Draw roads
        for name, intersection in city.intersections.items():
            x1, y1 = self.get_pixel_coords(name)
            for neighbor in intersection.neighbors:
                x2, y2 = self.get_pixel_coords(neighbor)
                pygame.draw.line(self.screen, (100, 100, 100), (x1, y1), (x2, y2), ROAD_WIDTH)

        # 2. Draw intersections (traffic lights)
        for name in city.intersections:
            x, y = self.get_pixel_coords(name)
            color = self.get_intersection_color(name)  # Live check every frame
            pygame.draw.circle(self.screen, color, (x, y), INTERSECTION_RADIUS)

        # 3. Draw cars (on top)
        for car in city.cars:
            x, y = car.get_position(self.get_pixel_coords)
            rect = pygame.Rect(0, 0, CAR_WIDTH, CAR_LENGTH)
            rect.center = (x, y)
            pygame.draw.rect(self.screen, (255, 100, 100), rect)

        pygame.display.flip()
        self.clock.tick(60)
