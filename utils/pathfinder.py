import heapq

def dijkstra_path(city, start, goal):
    heap = [(0, start, [start])]
    visited = set()

    while heap:
        cost, current, path = heapq.heappop(heap)
        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            return path

        for neighbor, weight in city.intersections[current].neighbors.items():
            if neighbor not in visited:
                heapq.heappush(heap, (cost + weight, neighbor, path + [neighbor]))

    return None