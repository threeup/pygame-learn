import pygame

from enty import Enty
from ctrlr import Ctrlr
from cnphy.vec2d import Vec2d


class AICtrlr(Ctrlr):
    def __init__(self, enty_list):
        # invoking the __init__ of the parent class
        Ctrlr.__init__(self, enty_list)
        self.delta_x = 0
        self.delta_y = 0
        self.score = 0
        for i in range(self.count):
            self.reset(self.list[i], i)

    def reset(self, enty, offset):
        enty.attach = None
        #enty.set_pos(0, random.randrange(300, 350))
        enty.set_pos(Vec2d(0, 300+5*offset))
        #enty.set_vel(random.randrange(8, 13), random.randrange(-5, 5))
        enty.set_fixed_vel(Vec2d(9, 1))

    def tick(self, _delta):
        for i in range(self.count):
            enty = self.list[i]
            enty_pos = enty.get_pos()
            atch = enty.attach
            if atch is not None:
                attack_pos = atch.get_pos()
                delta_dir, delta_mag = (
                    attack_pos-enty_pos).normalized_and_length()
                if delta_mag < 10:
                    self.score += 1
                    self.reset(enty, i)
                    continue

                spd = 4
                next_pos = enty_pos + delta_dir.scaled(spd)
                enty.set_pos(next_pos)
                continue

            if (enty_pos.x > 600):
                enty.set_pos(Vec2d(0, enty_pos.y))
                #enty.set_vel(random.randrange(8, 13), random.randrange(-5, 5))
                enty.set_fixed_vel(Vec2d(9, 1))
                continue

            vel = enty.get_fixed_vel()
            if enty_pos.y < 70 and vel.y < 0:
                enty.set_fixed_vel(Vec2d(vel.x, -vel.y))
                vel = enty.get_fixed_vel()
            elif enty_pos.y > 310 and vel.y > 0:
                enty.set_fixed_vel(Vec2d(vel.x, -vel.y))
                vel = enty.get_fixed_vel()
            spd = enty.fixed_speed
            enty.set_pos(Vec2d(enty_pos.x + spd*vel.x, enty_pos.y + spd*vel.y))
