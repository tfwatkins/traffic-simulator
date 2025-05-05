import random

class Intersection:
    def __init__(self, name, has_light=True):
        self.name = name
        self.has_light = has_light
        self.is_green = random.choice([True, False]) if has_light else True
        self.last_switch_tick = 0
        self.neighbors = {}
