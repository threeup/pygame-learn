import math


class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vec2(x, y)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Vec2(x, y)

    def __truediv__(self, other):
        x = self.x / other
        y = self.y / other
        return Vec2(x, y)

    def __len__(self):
        return 2

    def to_tuple(self):
        return (self.x, self.y)

    def rotated(self, angle):
        x = self.x * math.cos(angle) - self.y*math.sin(angle)
        y = self.y * math.sin(angle) - self.x*math.cos(angle)
        return Vec2(x, y)

    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    def scaled(self, scale):
        return Vec2(self.x*scale, self.y*scale)

    def test(self, scale):
        return scale

    def normalized(self):
        vec_len = self.length()
        return self/vec_len

    def normalized_and_length(self):
        vec_len = self.length()
        vec_dir = self.scaled(1/vec_len)
        return (vec_dir, vec_len)
