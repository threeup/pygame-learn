from cnphy.vec2d import Vec2d

class Body(object):
    STATIC = 100,
    KINEMATIC = 101, 
    DYNAMIC = 102,

    def __init__(self, weight, body_type):
        self.size = 0
        self.body_type = body_type
        self.position = Vec2d(0,0)
        self.velocity = Vec2d(0,0)
        self.angle = 90

    def set_pos(self, pos):
        self.position.x = pos.x
        self.position.y = pos.y
