''' holds EntyCircle class '''
import pygame
from enty import Enty

from cnphy.body import Body
from cnphy.shape import Circle


class EntyCircle(Enty):
    '''
    A class which represents a base movable drawable circular entity
    '''
    def __init__(self, name, color, radius, path):
        Enty.__init__(self, name)
        self.radius = radius
        self.color = color
        if path:
            raw_img = pygame.image.load(path)
            self.img = pygame.transform.scale(
                raw_img, (2*self.radius, 2*self.radius))
        else:
            self.img = None

    def tick(self, delta):
        '''an event which represents time elapsed'''
        Enty.tick(self, delta)
        if self.grounded is False:
            self.heading = (self.heading + 3) % 360

    def rot_center(self, image, angle):
        '''rotate an image while keeping its center and size'''
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def draw(self, screen, flipy):
        '''draws a circle using drawing library'''
        enty_pos = self.get_pos()
        if self.img:
            enty_center = self.img.get_rect().center
            draw_x = int(enty_pos.x) - enty_center[0]
            draw_y = int(flipy(enty_pos.y)) - enty_center[1]
            rot_img = self.rot_center(self.img, self.heading)
            screen.blit(rot_img, (draw_x, draw_y))
        else:
            draw_pos = int(enty_pos.x), int(flipy(enty_pos.y))
            pygame.draw.circle(screen, self.color, draw_pos,
                               int(self.radius), 5)

    def add_collision(self, space, pos, bodtype, coltype):
        '''create physics classes and attached to the physics simulation'''
        self.body = Body(space, 1666, bodtype)
        self.body.set_pos(pos)
        self.shape = Circle(self.body.munkbody, coltype, self.radius)
        self.shape.owner = self
        space.add(self.body, self.shape)
