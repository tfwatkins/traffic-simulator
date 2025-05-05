# test_graph.py

import pygame
import sys

from map.city_graph import CityGraph
from utils.visualizer import Visualizer
from vehicles.car import Car
from vehicles.spawner import CarSpawner
from utils.pathfinder import dijkstra_path
from signals.controller import TrafficController

def main():
    grid_size = 16
    city = CityGraph()
    city.load_grid(size=grid_size)

    # Initialize traffic controller AFTER grid is fully constructed
    traffic = TrafficController(city, cycle_interval=180)

    # Only initialize these AFTER traffic controller is set
    visualizer = Visualizer(city)
    spawner = CarSpawner(city, grid_size=grid_size, spawn_interval=30)

    tick = 0
    running = True

    while running:
        tick += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update traffic lights
        traffic.update(tick)

        # Spawn new cars
        spawner.update(tick)

        # Move cars forward
        for car in city.cars:
            car.update(city=city)

        # Render city and vehicles
        visualizer.render(city, tick)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
