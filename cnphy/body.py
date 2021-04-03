import pymunk


class Body(object):
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
        if self.munkbody.body_type == pymunk.Body.STATIC:
            return self.STATIC
        elif self.munkbody.body_type == pymunk.Body.KINEMATIC:
            return self.KINEMATIC
        elif self.munkbody.body_type == pymunk.Body.DYNAMIC:
            return self.DYNAMIC

    def get_mass(self):
        return self.munkbody.mass

    def set_pos(self, pos):
        self.munkbody.position = pos.x, pos.y

    def set_vel(self, vel):
        self.munkbody.velocity = vel.x, vel.y

    def impulse(self, vec):
        self.munkbody.apply_impulse_at_local_point(vec.to_tuple())

    def get_pos(self):
        return self.munkbody.position
