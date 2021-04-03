import pygame

from cnphy.vec2d import Vec2d


class Enty:
    def __init__(self, name):
        self.name = name
        self.grounded = False
        self.elapsed_time = 0
        self.fixed_vel = Vec2d(0, 0)
        self.fixed_speed = 0.2
        self.debug = False
        self.body = None
        self.shape = None
        self.attach = None

    def set_fixed_vel(self, vel):
        self.fixed_vel = vel

    def get_fixed_vel(self):
        return self.fixed_vel

    def set_pos(self, pos):
        if self.body:
            self.grounded = True
            self.body.set_vel(Vec2d(0, 0))
            self.body.set_pos(pos)

    def get_pos(self):
        if self.body:
            return self.body.get_pos()
        return Vec2d(0, 0)

    def impulse(self, vec):
        if self.body:
            self.grounded = False
            self.body.impulse(vec.scaled(self.body.get_mass()))

    def tick(self, delta):
        self.elapsed_time += delta

    def draw(self, screen, flipy):
        ent_pos = self.get_pos()
        color = pygame.Color("red")
        draw_pos = int(ent_pos.x), int(flipy(ent_pos.y))
        pygame.draw.circle(screen, color, draw_pos, 30, 12)
