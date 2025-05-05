# Urban Traffic Simulator

This is a Pygame-based traffic simulation demonstrating basic traffic light control, car queuing, and congestion-aware rerouting using a Quadtree.

## Features

- **Grid-Based City**: A 16x16 grid of intersections connected via bidirectional roads.
- **Traffic Lights**: Half of the intersections are randomly assigned traffic lights. Cars obey red lights.
- **Cars**: Cars spawn randomly at the grid edges and attempt to reach an opposite edge using Dijkstra's algorithm.
- **Quadtree Traffic Awareness**: Cars use a quadtree to detect local congestion and avoid colliding or jamming too close to others.
- **Queueing**: Vehicles form queues at red lights with small gaps between them.
- **Visualization**: Green, red, and gray dots represent light states; cars are rendered as rectangles.

## Algorithms Used

- **Dijkstra's Algorithm**: Used for initial route planning between entry and exit nodes.
- **Quadtree**: For spatial partitioning and efficient lookup of nearby vehicles.
- **Basic State Machine**: Used for signal light timing and control.

## File Overview

- `test_graph.py`: Main entry point and simulation loop.
- `map/city_graph.py`: Grid construction, road/intersection modeling.
- `signals/intersection.py`: Traffic light and intersection logic.
- `signals/controller.py`: Global traffic light timing updates.
- `vehicles/car.py`: Car behavior, queuing, and collision avoidance.
- `vehicles/spawner.py`: Logic for periodic vehicle spawning.
- `utils/pathfinder.py`: Dijkstra pathfinding logic.
- `utils/quadtree.py`: Spatial structure for car proximity detection.
- `utils/visualizer.py`: All rendering logic.

## How to Run

```bash
python3 test_graph.py
```

Requires Python 3.12+ and pygame 2.6+.
