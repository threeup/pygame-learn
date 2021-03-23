import pygame
import numpy as np
import scipy.io.wavfile as siow
from enty import Enty

SAMPLERATE = 44100

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
        self.sfx_down = []
        self.sfx_up = []

        for i in range(self.count):
            self.held.append(False)
            self.sfx_down.append(self.make_tone(100+i*100))
            self.sfx_up.append(self.make_tone(150+i*100))

    def make_tone(self, freq=1000, volume=10000, length=1):
        
        num_steps = int(length*SAMPLERATE)
        intro = int(length*SAMPLERATE*0.2)
        s = []

        for n in range(num_steps):
            value = np.sin(n * freq * (6.28318/SAMPLERATE) * length)*volume
            if n < intro:
                ease = n/intro
                s.append([value*ease, value*ease])
            elif (num_steps-n) < intro:
                ease = (num_steps-n)/intro
                s.append([value*ease, value*ease])
            else:
                s.append([value, value])
        buffer = np.array(s)
        return pygame.sndarray.make_sound(buffer.astype(np.int16))

    def load_sound(self, name):
        _, buffer = siow.read(name)
        buffer = np.repeat(buffer.reshape(len(buffer), 1), 2, axis=1)
        return pygame.sndarray.make_sound(buffer)

    def handle_event(self, event):
        if event.type == pygame.JOYBUTTONDOWN:
            for i in range(self.count):
                if event.button == i:
                    self.held[i] = True
                    self.sfx_down[i].set_volume(1)
                    self.sfx_down[i].play()
        elif event.type == pygame.JOYBUTTONUP:
            for i in range(self.count):
                if event.button == i:
                    self.held[i] = False
                    self.sfx_up[i].set_volume(1)
                    self.sfx_up[i].play()

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
        for i in range(self.count):
            p = self.list[i].get_pos()
            if p.y < 100:
                self.list[i].set_pos(p.x, 100)
            elif(p.x < 600):
                self.list[i].set_pos(p.x+10, p.y)
            else:
                self.list[i].set_pos(0, p.y)
