import pygame
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

    def draw(self, screen, flipy):
        draw_pos = int(self.p.x), int(flipy(self.p.y))
        pygame.draw.circle(screen, self.color, draw_pos, int(self.radius), 12)

    def addCircleCollision(self, space, btype):
        self.body = pymunk.Body(body_type = btype)
        self.shape = pymunk.Circle(self.body, 30, (0, 0))
        self.shape.collision_type = 1
        space.add(self.body)
