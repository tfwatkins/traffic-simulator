# utils/quadtree.py

class Quadtree:
    def __init__(self, x, y, width, height, capacity=4):
        self.boundary = (x, y, width, height)
        self.capacity = capacity
        self.points = []
        self.divided = False

    def insert(self, point, data=None):
        x, y, w, h = self.boundary
        px, py = point

        if not (x <= px < x + w and y <= py < y + h):
            return False

        if len(self.points) < self.capacity:
            self.points.append((point, data))
            return True
        else:
            if not self.divided:
                self.subdivide()
            return (
                self.nw.insert(point, data) or
                self.ne.insert(point, data) or
                self.sw.insert(point, data) or
                self.se.insert(point, data)
            )

    def subdivide(self):
        x, y, w, h = self.boundary
        hw, hh = w / 2, h / 2
        self.nw = Quadtree(x, y, hw, hh, self.capacity)
        self.ne = Quadtree(x + hw, y, hw, hh, self.capacity)
        self.sw = Quadtree(x, y + hh, hw, hh, self.capacity)
        self.se = Quadtree(x + hw, y + hh, hw, hh, self.capacity)
        self.divided = True

    def query_range(self, range_box):
        found = []
        x, y, w, h = self.boundary
        rx, ry, rw, rh = range_box

        if not self._intersects(range_box):
            return found

        for (px, py), data in self.points:
            if rx <= px <= rx + rw and ry <= py <= ry + rh:
                found.append(data)

        if self.divided:
            found.extend(self.nw.query_range(range_box))
            found.extend(self.ne.query_range(range_box))
            found.extend(self.sw.query_range(range_box))
            found.extend(self.se.query_range(range_box))

        return found

    def _intersects(self, range_box):
        x, y, w, h = self.boundary
        rx, ry, rw, rh = range_box
        return not (rx > x + w or rx + rw < x or ry > y + h or ry + rh < y)
