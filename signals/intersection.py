# 2. signals/intersection.py

import random

class Intersection:
    def __init__(self, name):
        self.name = name
        self.is_green = random.choice([True, False])
        self.last_switch_tick = 0
        self.neighbors = {}