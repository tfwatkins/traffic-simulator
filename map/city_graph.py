# map/city_graph.py

from signals.intersection import Intersection

class CityGraph:
    def __init__(self):
        self.intersections = {}  # name -> Intersection object
        self.cars = []

    def add_intersection(self, name):
        if name not in self.intersections:
            self.intersections[name] = Intersection(name)

    def add_road(self, from_name, to_name, weight=1):
        self.add_intersection(from_name)
        self.add_intersection(to_name)
        # In simplified mode, no neighbor logic is required
        self.intersections[from_name].neighbors[to_name] = weight
        self.intersections[to_name].neighbors[from_name] = weight

    def load_grid(self, size=5):
        for y in range(size):
            for x in range(size):
                name = f"{x},{y}"
                self.add_intersection(name)
                if x > 0:
                    self.add_road(name, f"{x-1},{y}")
                if y > 0:
                    self.add_road(name, f"{x},{y-1}")
