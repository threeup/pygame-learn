from cnphy.vec2d import Vec2d

class Shape(object):

    def __init__(self, body, collision_type):
        self.size = 0
        self.body = body
        self.collision_type = collision_type
        self.owner = None

class Segment(Shape):
    def __init__(self, body, collision_type, pt1, pt2):
        Shape.__init__(self, body, collision_type)
        self.pt1 = pt1
        self.pt2 = pt2

class Circle(Shape):
    def __init__(self, body, collision_type, radius):
        Shape.__init__(self, body, collision_type)
        self.radius = radius