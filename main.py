from map.city_graph import CityGraph
from vehicles.spawner import CarSpawner
from signals.controller import TrafficController
from simulation.clock import SimulationClock
from utils.visualizer import Visualizer

TICK_DURATION = 0.1 # seconds per tick
TOTAL_TICKS = 1000

def main():
    # Setup phase
    city = CityGraph()
    city.load_grid(size=5) 

    spawner = CarSpawner(city)
    traffic_controller = TrafficController(city)
    visualizer = Visualizer(city)

    clock = SimulationClock(tick_duration=TICK_DURATION)

    # Simulation loop
    for tick in range(TOTAL_TICKS):
        print(f"Tick: {tick}")

        # 1. possibly spawn car
        spawner.update(tick)

        # 2. update traffic lights at intersection
        traffic_controller.update(tick)

        # 3. move all cars
        for car in city.cars:
            car.move(city)

        # 4. visual update
        visualizer.render(city, tick)

        # 5. wait for next tick
        clock.sleep()

if __name__ == "__main__":
    main()

