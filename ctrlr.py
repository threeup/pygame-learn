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
    def __init__(self, enty_list):
        # invoking the __init__ of the parent class
        Ctrlr.__init__(self, enty_list)
        self.held = []
        self.sound_effect = pygame.mixer.Sound('brr.wav')

        for _ in range(self.count):
            self.held.append(False)

    def handle_event(self, event):
        if event.type == pygame.JOYBUTTONDOWN:
            self.sound_effect.play()
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
                    self.list[i].impulse(0, 30)
            else:
                if p.y < 100:
                    self.list[i].set_pos(p.x, 100)
        return


class AICtrlr(Ctrlr):
    def __init__(self, enty_list):
        # invoking the __init__ of the parent class
        Ctrlr.__init__(self, enty_list)
        self.delta_x = 0
        self.delta_y = 0

    def tick(self, deltaTime):
        first_enty = self.list[0]
        if self.delta_x == 0 and self.delta_y == 0:
            self.delta_x = 2
        elif self.delta_x == 2:
            if first_enty.p.y > 280:
                self.delta_x = -2
                self.delta_y = 0
            elif self.delta_y == 0 and first_enty.p.x > 400:
                self.delta_y = 5
        else:
            if first_enty.p.y < 100:
                self.delta_x = 2
                self.delta_y = 0
            elif self.delta_y == 0 and first_enty.p.x < 200:
                self.delta_y = -5
        first_enty.move(self.delta_x, self.delta_y)
