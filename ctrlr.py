import pygame

from enty import Enty


class Ctrlr:
    def __init__(self, enty):
        self.controlled = enty
        self.colc = pygame.Color("cyan")
        self.colg = pygame.Color("green")
        self.colb = pygame.Color("blue")
        self.coly = pygame.Color("yellow")
        self.colr = pygame.Color("red")
        self.col = self.colc
        self.delta_x = 0
        self.delta_y = 0

    def handle_event(self, event):
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0:
                self.col = self.colg
            elif event.button == 1:
                self.col = self.colr
            elif event.button == 2:
                self.col = self.coly
            elif event.button == 3:
                self.col = self.colb
        elif event.type == pygame.JOYBUTTONUP:
            self.col = self.colc

    def tick(self, deltaTime):
        if self.delta_x == 0 and self.delta_y == 0:
            self.delta_x = 1
        elif self.delta_x == 1:
            if self.controlled.p.y > 450:
                self.delta_x = -1
                self.delta_y = 0
            elif self.delta_y == 0 and self.controlled.p.x > 400:
                self.delta_y = 3
        else:
            if self.controlled.p.y < 100:
                self.delta_x = 1
                self.delta_y = 0
            elif self.delta_y == 0 and self.controlled.p.x < 200:
                self.delta_y = -3
        self.controlled.move(self.delta_x, self.delta_y)
