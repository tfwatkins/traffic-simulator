# test_graph.py

import pygame
import sys
from map.city_graph import CityGraph
from utils.visualizer import Visualizer
from vehicles.spawner import CarSpawner
from signals.controller import TrafficController
from utils.quadtree import Quadtree

WINDOW_SIZE = 1600

def main():
    grid_size = 16
    city = CityGraph()
    city.load_grid(size=grid_size)

    traffic = TrafficController(city, cycle_interval=180)
    visualizer = Visualizer(city, width=WINDOW_SIZE, height=WINDOW_SIZE)
    spawner = CarSpawner(city, grid_size=grid_size, spawn_interval=30)

    tick = 0
    running = True

    while running:
        tick += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        traffic.update(tick)
        spawner.update(tick)

        # Create quadtree
        quadtree = Quadtree(0, 0, WINDOW_SIZE, WINDOW_SIZE)
        for car in city.cars:
            x, y = car.get_position(visualizer.get_pixel_coords)
            quadtree.insert((x, y), car)

        for car in city.cars:
            car.update(city=city, cars=city.cars,
                       pixel_coords_func=visualizer.get_pixel_coords,
                       quadtree=quadtree)

        visualizer.render(city, tick)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
