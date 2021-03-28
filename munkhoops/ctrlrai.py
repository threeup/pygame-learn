import pygame
import random
from pymunk import Vec2d

from enty import Enty
from ctrlr import Ctrlr


class AICtrlr(Ctrlr):
    def __init__(self, enty_list):
        # invoking the __init__ of the parent class
        Ctrlr.__init__(self, enty_list)
        self.delta_x = 0
        self.delta_y = 0
        self.score = 0
        for i in range(self.count):
            self.reset(self.list[i])

    def reset(self, enty):
        enty.attach = None
        enty.set_pos(0, random.randrange(300, 350))
        enty.set_vel(random.randrange(8, 13), random.randrange(-5, 5))

    def tick(self, deltaTime):
        for i in range(self.count):
            enty = self.list[i]
            p = enty.get_pos()
            atch = enty.attach
            if atch != None:
                ap = atch.get_pos()
                delta = Vec2d(ap.x-p.x, ap.y-p.y)
                delta_dir, delta_mag = delta.normalized_and_length()
                if delta_mag < 10:
                    self.score += 1
                    self.reset(enty)
                    continue

                spd = 4
                enty.set_pos(p.x + spd*delta_dir.x, p.y + spd*delta_dir.y)
                continue

            if (p.x > 600):
                enty.set_pos(0, p.y)
                enty.set_vel(random.randrange(8, 13), random.randrange(-5, 5))
                continue

            v = enty.get_vel()
            if p.y < 70 and v.y < 0:
                enty.set_vel(v.x, -v.y)
                v = enty.get_vel()
            elif p.y > 310 and v.y > 0:
                enty.set_vel(v.x, -v.y)
                v = enty.get_vel()
            spd = enty.fixed_speed
            enty.set_pos(p.x + spd*v.x, p.y + spd*v.y)
