import random
from vehicles.car import Car
from utils.pathfinder import dijkstra_path

class CarSpawner:
    def __init__(self, city, grid_size, spawn_interval=30):
        self.city = city
        self.grid_size = grid_size
        self.spawn_interval = spawn_interval
        self.edges = self._get_edge_nodes(grid_size)

    def _get_edge_nodes(self, size):
        return {
            'top':    [f"{x},0" for x in range(size)],
            'bottom': [f"{x},{size-1}" for x in range(size)],
            'left':   [f"0,{y}" for y in range(size)],
            'right':  [f"{size-1},{y}" for y in range(size)],
        }

    def update(self, tick):
        if tick % self.spawn_interval != 0:
            return

        source_edge = random.choice(list(self.edges.keys()))
        source = random.choice(self.edges[source_edge])

        dest_edge = random.choice([k for k in self.edges if k != source_edge])
        destination = random.choice(self.edges[dest_edge])

        path = dijkstra_path(self.city, source, destination)
        if path:
            car = Car(path, speed=1)
            self.city.cars.append(car)