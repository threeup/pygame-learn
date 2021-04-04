''' holds Enty class '''
import pygame

from cnphy.vec2 import Vec2


class Enty:
    '''
    A class which represents a base movable drawable entity
    '''
    def __init__(self, name):
        self.name = name
        self.grounded = False
        self.elapsed_time = 0
        self.fixed_vel = Vec2(0, 0)
        self.fixed_speed = 0.2
        self.debug = False
        self.body = None
        self.shape = None
        self.attach = None

    def set_fixed_vel(self, vel):
        '''
        assign a fixed velocity which will not change on its own
        > (Vec2)
        '''
        self.fixed_vel = vel

    def get_fixed_vel(self):
        '''
        retrieve the fixed velocity
        < (Vec2)
        '''
        return self.fixed_vel

    def set_pos(self, pos):
        '''
        assign a position, requires physics body
        > (Vec2)
        '''
        if self.body:
            self.grounded = True
            self.body.set_vel(Vec2(0, 0))
            self.body.set_pos(pos)

    def get_pos(self):
        '''
        returns a position, requires physics body
        < (Vec2)
        '''
        if self.body:
            return self.body.get_pos()
        return Vec2(0, 0)

    def impulse(self, vec):
        '''
        apply an impulse, requires physics body
        > (Vec2)
        '''
        if self.body:
            self.grounded = False
            self.body.impulse(vec.scaled(self.body.get_mass()))

    def tick(self, delta):
        '''
        an event which represents time elapsed
        > (float)
        '''
        self.elapsed_time += delta

    def draw(self, screen, flipy):
        '''
        a basic drawing fallback
        > ()
        '''
        ent_pos = self.get_pos()
        color = pygame.Color("red")
        draw_pos = int(ent_pos.x), int(flipy(ent_pos.y))
        pygame.draw.circle(screen, color, draw_pos, 30, 12)
