from cnphy.body import Body


class Space(object):
    def __init__(self):
        self.bodies = []
        self.shapes = []
        self.funcs = []
        self.gravity = (0,0)
        self.time = 0
        self.static_body = Body(-1, Body.STATIC)
    
    def add(self, body, shape):
        self.bodies.append(body)
        self.shapes.append(shape)

    def add_collision_handler(self, a, b, func):
        self.funcs.append(func)

    def step(self, dt):
        self.time += dt