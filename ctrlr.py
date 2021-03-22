import pygame
import numpy as np
import scipy.io as sio
import scipy.io.wavfile as siow
import librosa
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

        brr_start = 4
        brr_factor = 6

        for i in range(self.count):
            self.held.append(False)
            self.sfx_down.append(self.load_sound(
                "brr.wav", brr_start + i * brr_factor))
            self.sfx_up.append(self.load_sound(
                "brr.wav", brr_start + brr_factor / 2 + i * brr_factor))
            # self.sfx_down.append(self.make_tone(100+i*100))
            # self.sfx_up.append(self.make_tone(150+i*100))

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

    def make_noise(self, pitch):
        xlen = 1
        buffer = np.sin(np.pi * np.arange(SAMPLERATE*xlen) *
                        pitch / SAMPLERATE).astype(np.float32)
        if pitch != 0:
            buffer = librosa.effects.pitch_shift(buffer, SAMPLERATE, n_steps=pitch)
            #buffer = librosa.effects.time_stretch(buffer, 1)

        buffer = np.repeat(buffer.reshape(len(buffer), 1), 2, axis=1)
        return pygame.sndarray.make_sound(buffer)

    def load_sound(self, name, pitch):
        sr, buffer = siow.read(name)
        if pitch != 0:
            buffer = buffer / np.float32(32767.0)
            buffer = librosa.effects.pitch_shift(buffer, sr, n_steps=pitch)
            buffer = buffer * np.float32(32767.0)
            buffer = buffer.astype(np.int16)

        buffer = np.repeat(buffer.reshape(len(buffer), 1), 2, axis=1)
        return pygame.sndarray.make_sound(buffer)

    def handle_event(self, event):
        if event.type == pygame.JOYBUTTONDOWN:
            for i in range(self.count):
                if event.button == i:
                    self.held[i] = True
                    # self.sfx_up[i].set_volume(0.9)
                    self.sfx_down[i].set_volume(1)
                    self.sfx_down[i].play()
        elif event.type == pygame.JOYBUTTONUP:
            for i in range(self.count):
                if event.button == i:
                    self.held[i] = False
                    # self.sfx_down[i].set_volume(0.9)
                    self.sfx_up[i].set_volume(1)
                    self.sfx_up[i].play()

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
