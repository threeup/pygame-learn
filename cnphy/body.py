''' holds body class '''
import pymunk
from cnphy.vec2 import Vec2


class Body(object):
    '''
    A class to represent a physics body
    '''
    STATIC = 100,
    KINEMATIC = 101,
    DYNAMIC = 102,

    def __init__(self, space, weight, body_type):
        if body_type == self.STATIC:
            munk_type = pymunk.Body.STATIC
            self.munkbody = space.get_static_body()
        elif body_type == self.KINEMATIC:
            munk_type = pymunk.Body.KINEMATIC
            self.munkbody = pymunk.Body(1, weight, munk_type)
        elif body_type == self.DYNAMIC:
            munk_type = pymunk.Body.DYNAMIC
            self.munkbody = pymunk.Body(1, weight, munk_type)
        self.munkbody.cnbody = self
        self.init = True

    def get_body_type(self):
        '''
        Returns the type in cn foormat
        < (cnbody.Body.STATIC | KINEMATIC | DYNAMIC)
        '''
        if self.munkbody.body_type == pymunk.Body.STATIC:
            return self.STATIC
        elif self.munkbody.body_type == pymunk.Body.KINEMATIC:
            return self.KINEMATIC
        elif self.munkbody.body_type == pymunk.Body.DYNAMIC:
            return self.DYNAMIC

    def get_mass(self):
        '''
        Returns the mass
        < (float)
        '''
        return self.munkbody.mass

    def set_pos(self, pos):
        '''
        Assigns a position
        > (Vec2)
        '''
        self.munkbody.position = pos.x, pos.y

    def set_vel(self, vel):
        '''
        Assigns a velocity
        > (Vec2)
        '''
        self.munkbody.velocity = vel.x, vel.y

    def impulse(self, vec):
        '''
        Applies an impules at a local point
        > (Vec2)
        '''
        self.munkbody.apply_impulse_at_local_point(vec.to_tuple())

    def get_pos(self):
        '''
        Returns the position
        < (Vec2)
        '''
        munkpos = self.munkbody.position
        return Vec2(munkpos.x, munkpos.y)

    
    def get_vel(self):
        '''
        Returns the velocity
        < (Vec2)
        '''
        munkvel = self.munkbody.velocity
        return Vec2(munkvel.x, munkvel.y)
