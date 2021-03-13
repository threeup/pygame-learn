
import pymunk
from pymunk import Vec2d

class Enty:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.radius = 50
        self.p =  Vec2d(0,0)
        self.elapsed_time = 0

        
    def set_pos(self, x, y):
        self.p = Vec2d(x, y)

    def move(self, x, y):
        self.p = Vec2d(self.p.x + x, self.p.y + y)

    def tick(self, delta):
        self.elapsed_time += delta

    def get_draw_pos(self, flip):
        return int(self.p.x), int(flip(self.p.y))