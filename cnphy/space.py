''' holds space class '''
import pymunk


class Space(object):
    '''
    A class to represent a physics environment with shapes and bodies
    '''
    def __init__(self):
        self.munkspace = pymunk.Space()
        self.munkspace.gravity = 0.0, -981.0

    def add(self, body, shape):
        '''
        Returns the type in cn foormat
        (cnbody.Body.STATIC | KINEMATIC | DYNAMIC)
        '''
        if body is not None:
            self.munkspace.add(body.munkbody, shape.munkshape)
        else:
            self.munkspace.add(shape.munkshape)

    def add_collision_handler(self, type1, type2, func):
        '''
        Adds a collision handler function
        > (type, type, func)
        '''
        self.munkspace.add_collision_handler(type1, type2).pre_solve =  func

    def get_static_body(self):
        '''
        Retrieves the static body from the backing lib
        > (munk body)
        '''
        return self.munkspace.static_body

    def aabboverlap(self, lhs, rhs):
        '''
        Checks two axis aligned bounding box and returns true when they overlap
        > (bool)
        '''
        box_lhs = lhs.aabb()
        box_rhs = rhs.aabb()
        x_left = max(box_lhs.start.x, box_rhs.start.x)
        y_top = max(box_lhs.start.y, box_rhs.start.y)
        x_right = min(box_lhs.end.x, box_rhs.end.x)
        y_bottom = min(box_lhs.end.y, box_rhs.end.y)
        return x_right > x_left and y_bottom > y_top

    def step(self, delta):
        '''
        Increments the physics simulation by one step
        > (float)
        '''
        self.munkspace.step(delta)
