import pygame
import pymunk
from pymunk import Vec2d
from enty import Enty


class CircEnty(Enty):
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
                               int(self.radius), 12)

    def addCollision(self, space, pos, btype):
        self.body = pymunk.Body(1, 1666, body_type=btype)
        self.body.position = pos[0], pos[1]
        self.shape = pymunk.Circle(self.body, self.radius, (0, 0))
        space.add(self.body, self.shape)
