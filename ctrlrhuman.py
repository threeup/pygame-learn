''' holds MouseCtrlr and HumanCtrlr class '''
import pygame
from ctrlr import Ctrlr
from cnphy.vec2 import Vec2

class MouseCtrlr(Ctrlr):
    '''
    A class which manipulates controlled entities using the mouse
    '''
    def __init__(self, flipy):
        self.mousep = [0, 0]
        self.flipy = flipy
        # invoking the __init__ of the parent class
        Ctrlr.__init__(self)

    def handle_event(self, _event):
        '''Respond to event, grabs mouse position'''
        self.mousep = pygame.mouse.get_pos()

    def tick(self, _delta):
        '''Manipulates the first controlled entity to the mouse position'''
        first_enty = self.list[0]
        first_enty.set_pos(Vec2(self.mousep[0], self.flipy(self.mousep[1])))


class HumanCtrlr(Ctrlr):
    '''
    A class which manipulates controlled entities using human input events
    '''
    def __init__(self):
        # invoking the __init__ of the parent class
        Ctrlr.__init__(self)
        self.held = []

    def add_enty(self, enty):
        Ctrlr.add_enty(self, enty)
        self.held.append(False)

    def handle_event(self, event):
        '''Respond to event, grabs joystick state'''
        if event.type == pygame.JOYBUTTONDOWN:
            for i in range(self.count):
                if event.button == i:
                    self.held[i] = True
        elif event.type == pygame.JOYBUTTONUP:
            for i in range(self.count):
                if event.button == i:
                    self.held[i] = False

    def tick(self, _delta):
        '''Manipulates the all controlled entities based on inputs and limits'''
        for i in range(self.count):
            position = self.list[i].get_pos()
            if self.held[i]:
                if position.y < 320:
                    home_x = 200+110*i
                    delta_x = home_x-position.x
                    impulse_x = max(-10, min(0.25*delta_x, 10))
                    self.list[i].impulse(Vec2(impulse_x, 30))
            else:
                if position.y < 60:
                    self.list[i].set_pos(Vec2(position.x, 60))
        return
