import pygame
import pymunk
from pymunk import Vec2d

class Enty:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.radius = 50
        self.elapsed_time = 0
        self.debug = False

        
    def set_pos(self, x, y):
        if self.body:
            self.body.velocity = Vec2d(0,0)
            self.body.position = x,y

    def get_pos(self):
        if self.body:
            return self.body.position
        return (0,0)

    def impulse(self, x, y):
        if self.body:
            impulse = (self.body.mass * x,self.body.mass * y)
            self.body.apply_impulse_at_local_point(impulse)

    def tick(self, delta):
        self.elapsed_time += delta

    def draw(self, screen, flipy):
        p = self.body.position
        draw_pos = int(p.x), int(flipy(p.y))
        pygame.draw.circle(screen, self.color, draw_pos, int(self.radius), 12)

    def addCircleCollision(self, space, pos, btype):
        self.body = pymunk.Body(1,1666,body_type = btype)
        self.body.position = pos[0],pos[1]
        self.shape = pymunk.Circle(self.body, 30, (0, 0))
        space.add(self.body, self.shape)
