import math


class Vec2d:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vec2d(x, y)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Vec2d(x, y)

    def __truediv__(self, other):
        x = self.x / other
        y = self.y / other
        return Vec2d(x, y)

    def rotated(self, angle):
        x = self.x * math.cos(angle) - self.y*math.sin(angle)
        y = self.y * math.sin(angle) - self.x*math.cos(angle)
        return Vec2d(x, y)

    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    def normalized(self):
        len = self.length()
        return self/len

    def normalized_and_length(self):
        len = self.length()
        dir = self/len
        return (dir, len)
