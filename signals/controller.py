class TrafficController:
    def __init__(self, city, cycle_interval=60):
        self.city = city
        self.cycle_interval = cycle_interval
        
    def update(self, tick):
        for intersection in self.city.intersections.values():
            if tick - intersection.last_switch_tick >= self.cycle_interval:
                intersection.is_green = not intersection.is_green
                intersection.last_switch_tick = tick