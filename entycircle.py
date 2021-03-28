import pygame
from enty import Enty

from cnphy.body import Body
from cnphy.shape import Shape, Circle
from cnphy.space import Space
from cnphy.vec2d import Vec2d


class EntyCircle(Enty):
    def __init__(self, name, color, radius, path):
        Enty.__init__(self, name)
        self.radius = radius
        self.heading = 0
        self.color = color
        if path:
            raw_img = pygame.image.load(path)
            self.img = pygame.transform.scale(
                raw_img, (2*self.radius, 2*self.radius))
        else:
            self.img = None
            


    def tick(self, delta):
        Enty.tick(self, delta)
        if self.grounded == False:
            self.heading = (self.heading + 3) % 360

    def rot_center(self, image, angle):
        """rotate an image while keeping its center and size"""
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def draw(self, screen, flipy):
        p = self.get_pos()
        if self.img:
            c = self.img.get_rect().center
            draw_x = int(p.x) - c[0]
            draw_y = int(flipy(p.y)) - c[1]
            rot_img = self.rot_center(self.img, self.heading)
            screen.blit(rot_img, (draw_x, draw_y))
        else:
            draw_pos = int(p.x), int(flipy(p.y))
            pygame.draw.circle(screen, self.color, draw_pos,
                               int(self.radius), 5)

    def addCollision(self, space, pos, bodtype, coltype):
        self.body = Body(1666, bodtype)
        self.body.set_pos(pos)
        self.shape = Circle(self.body, coltype, self.radius)
        self.shape.owner = self
        space.add(self.body, self.shape)
