import pymunk
from cnphy.vec2d import Vec2d


class Shape(object):

    def __init__(self, body, collision_type):
        self.size = 0
        self.body = body
        self.offset_pos = Vec2d(0, 0)
        self.collision_type = collision_type
        self.owner = None

    def aabb(self):
        pos = self.body.position + self.offset_pos
        return {'start': Vec2d(pos.x-1, pos.y-1),
                'end': Vec2d(pos.x+1, pos.y+1)}


class Segment():
    def __init__(self, body, collision_type, pt1, pt2):
        self.munkshape = pymunk.Segment(body, pt1.toTuple(), pt2.toTuple(), 0.1)
        self.munkshape.friction = 0.99
        self.munkshape.collision_type = collision_type
        self.munkshape.cnshape = self


class Circle():
    def __init__(self, body, collision_type, radius):
        self.munkshape = pymunk.Circle(body, radius, (0, 0))
        self.munkshape.collision_type = collision_type
        self.munkshape.cnshape = self
