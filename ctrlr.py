import pygame
from enty import Enty

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

    def handle_event(self, event):
        self.mousep = pygame.mouse.get_pos()

    def tick(self, deltaTime):
        first_enty = self.list[0]
        first_enty.set_pos(self.mousep[0], self.flipy(self.mousep[1]))


class HumanCtrlr(Ctrlr):
    def __init__(self, enty_list, samplerate):
        # invoking the __init__ of the parent class
        Ctrlr.__init__(self, enty_list)
        self.held = []
        for i in range(self.count):
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

    def tick(self, deltaTime):
        for i in range(self.count):
            p = self.list[i].get_pos()
            if self.held[i]:
                if p.y < 320:
                    home_x = 200+110*i
                    delta_x = home_x-p.x
                    impulse_x =  max(-10, min(0.25*delta_x, 10))
                    self.list[i].impulse(impulse_x, 30)
            else:
                if p.y < 60:
                    self.list[i].set_pos(p.x, 60)
        return


                
