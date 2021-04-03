import random

from ctrlr import Ctrlr
from cnphy.vec2 import Vec2


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
        enty.set_pos(Vec2(0, random.randrange(300, 350)))
        enty.set_fixed_vel(
            Vec2(random.randrange(8, 13),
                  random.randrange(-5, 5)))

    def tick(self, _delta):
        for i in range(self.count):
            enty = self.list[i]
            enty_pos = enty.get_pos()
            atch = enty.attach
            if atch is not None:
                delta = atch.get_pos() - enty_pos
                delta_dir, delta_mag = delta.normalized_and_length()
                if delta_mag < 10:
                    self.score += 1
                    self.reset(enty)
                    continue

                spd = 4

                scaled_dir = Vec2(delta_dir.x*spd, delta_dir.y*spd)
                next_pos = enty_pos + scaled_dir
                enty.set_pos(next_pos)
                continue

            if enty_pos.x > 600:
                enty.set_pos(Vec2(0, enty_pos.y))
                enty.set_fixed_vel(
                    Vec2(random.randrange(8, 13),
                          random.randrange(-5, 5)))
                continue

            vel = enty.get_fixed_vel()
            if enty_pos.y < 70 and vel.y < 0:
                enty.set_fixed_vel(Vec2(vel.x, -vel.y))
                vel = enty.get_fixed_vel()
            elif enty_pos.y > 310 and vel.y > 0:
                enty.set_fixed_vel(Vec2(vel.x, -vel.y))
                vel = enty.get_fixed_vel()
            spd = enty.fixed_speed
            enty.set_pos(Vec2(enty_pos.x + spd*vel.x, enty_pos.y + spd*vel.y))
