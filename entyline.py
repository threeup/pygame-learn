import pygame
from enty import Enty
from cnphy.body import Body
from cnphy.shape import Shape, Segment
from cnphy.space import Space
from cnphy.vec2d import Vec2d

class EntyLine(Enty):
    def __init__(self, name, color, path):
        Enty.__init__(self, name)
        self.length = 150
        self.width = 50
        self.color = color
        if path:
            raw_img = pygame.image.load(path)
            self.img = pygame.transform.scale(
                raw_img, (self.length, self.width))
        else:
            self.img = None

    def tick(self, delta):
        Enty.tick(self, delta)

    def draw(self, screen, flipy):
        body = self.shape.body
        p = body.position
        angl = body.angle
        if self.img:
            c = self.img.get_rect().center
            draw_x = int(p.x) - c[0]
            draw_y = int(flipy(p.y)) - c[1]
            draw_center = draw_x, draw_y
            screen.blit(self.img, draw_center)
        else:
            p1 = p + self.shape.pt1.rotated(angl)
            p2 = p + self.shape.pt2.rotated(angl)
            draw_p1 = int(p1.x), int(flipy(p1.y))
            draw_p2 = int(p2.x), int(flipy(p2.y))
            pygame.draw.lines(screen, self.color, False, [draw_p1, draw_p2], 4)

    def addCollision(self, space, pt1, pt2, bodtype, coltype):
        if bodtype == Body.STATIC:
            self.body = space.static_body
        else:
            self.body = Body(bodtype)
            
        self.shape = Segment(self.body, coltype, pt1, pt2)
        self.shape.owner = self
        space.add(self.body, self.shape)
