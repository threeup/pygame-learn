import pygame
import pymunk
from pymunk import Vec2d


class Enty:
    def __init__(self, name):
        self.name = name
        self.grounded = False
        self.elapsed_time = 0
        self.fixed_vel = Vec2d(0,0)
        self.fixed_speed = 0.2
        self.debug = False
        self.body = None
        self.attach = None

    def set_vel(self, x, y):
        self.fixed_vel = Vec2d(x,y)
    
    def get_vel(self):
        return self.fixed_vel

    def set_pos(self, x, y):
        if self.body:
            self.grounded = True
            self.body.velocity = Vec2d(0, 0)
            self.body.position = x, y

    def get_pos(self):
        if self.body:
            return self.body.position
        return Vec2d(0, 0)

    def impulse(self, x, y):
        if self.body:
            self.grounded = False
            impulse = (self.body.mass * x, self.body.mass * y)
            self.body.apply_impulse_at_local_point(impulse)

    def tick(self, delta):
        self.elapsed_time += delta


    def draw(self, screen, flipy):
        p = self.get_pos()
        color = pygame.Color("red")
        draw_pos = int(p.x), int(flipy(p.y))
        pygame.draw.circle(screen, color, draw_pos, 30, 12)
            

