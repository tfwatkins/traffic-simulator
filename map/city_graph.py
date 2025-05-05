from signals.intersection import Intersection
import random

class CityGraph:
    def __init__(self):
        self.intersections = {}  # name -> Intersection object
        self.cars = []

    def add_intersection(self, name, has_light=True):
        if name not in self.intersections:
            self.intersections[name] = Intersection(name, has_light=has_light)

    def add_road(self, from_name, to_name, weight=1):
        self.add_intersection(from_name)
        self.add_intersection(to_name)
        self.intersections[from_name].neighbors[to_name] = weight
        self.intersections[to_name].neighbors[from_name] = weight

    def load_grid(self, size=5):
        all_names = [f"{x},{y}" for y in range(size) for x in range(size)]
        no_light = set(random.sample(all_names, len(all_names) // 2))

        for y in range(size):
            for x in range(size):
                name = f"{x},{y}"
                has_light = name not in no_light
                self.add_intersection(name, has_light=has_light)
                if x > 0:
                    self.add_road(name, f"{x-1},{y}")
                if y > 0:
                    self.add_road(name, f"{x},{y-1}")
