import pygame
from enty import Enty
from cnphy.vec2d import Vec2d

class Ctrlr:
    def __init__(self, enty_list):
        self.count = len(enty_list)
        self.list = enty_list


class MouseCtrlr(Ctrlr):
    def __init__(self, enty_list, flipy):
        self.mousep = [0, 0]
        self.flipy = flipy
        # invoking the __init__ of the parent class
        Ctrlr.__init__(self, enty_list)

    def handle_event(self, _event):
        self.mousep = pygame.mouse.get_pos()

    def tick(self, _delta):
        first_enty = self.list[0]
        first_enty.set_pos(Vec2d(self.mousep[0], self.flipy(self.mousep[1])))


class HumanCtrlr(Ctrlr):
    def __init__(self, enty_list, _samplerate):
        # invoking the __init__ of the parent class
        Ctrlr.__init__(self, enty_list)
        self.held = []
        for _ in range(self.count):
            self.held.append(False)


    def handle_event(self, event):
        if event.type == pygame.JOYBUTTONDOWN:
            for i in range(self.count):
                if event.button == i:
                    self.held[i] = True
        elif event.type == pygame.JOYBUTTONUP:
            for i in range(self.count):
                if event.button == i:
                    self.held[i] = False

    def tick(self, _delta):
        for i in range(self.count):
            position = self.list[i].get_pos()
            if self.held[i]:
                if position.y < 320:
                    home_x = 200+110*i
                    delta_x = home_x-position.x
                    impulse_x =  max(-10, min(0.25*delta_x, 10))
                    self.list[i].impulse(Vec2d(impulse_x, 30))
            else:
                if position.y < 60:
                    self.list[i].set_pos(Vec2d(position.x, 60))
        return


                
