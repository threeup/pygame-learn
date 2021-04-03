import pygame
from enty import Enty
from cnphy.body import Body
from cnphy.shape import Segment


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
        munkshape = self.shape.munkshape
        munkbody = self.body.munkbody
        body_pos = munkbody.position
        body_angle = munkbody.angle
        if self.img:
            img_center = self.img.get_rect().center
            draw_x = int(body_pos.x) - img_center[0]
            draw_y = int(flipy(body_pos.y)) - img_center[1]
            draw_center = draw_x, draw_y
            screen.blit(self.img, draw_center)
        else:
            point1 = body_pos + munkshape.a.rotated(body_angle)
            point2 = body_pos + munkshape.b.rotated(body_angle)
            draw_point1 = int(point1.x), int(flipy(point1.y))
            draw_point2 = int(point2.x), int(flipy(point2.y))
            pygame.draw.lines(screen, self.color, False, [
                              draw_point1, draw_point2], 4)

    def add_collision(self, space, pt1, pt2, bodtype, coltype):
        self.body = Body(space, 2000, bodtype)
        self.shape = Segment(self.body.munkbody, coltype, pt1, pt2)
        self.shape.owner = self
        if bodtype == Body.STATIC:
            space.add(None, self.shape)
        else:
            space.add(self.body, self.shape)
