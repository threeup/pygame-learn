''' holds  HumanCtrlr class '''
import pygame
from ctrlr import Ctrlr
from cnphy.vec2 import Vec2



class HumanCtrlr(Ctrlr):
    '''
    A class which manipulates controlled entities using human input events
    '''
    def __init__(self, flipy):
        # invoking the __init__ of the parent class
        Ctrlr.__init__(self)
        self.flipy = flipy
        self.held = []
        self.pressed = []
        self.released = []
        self.hoops = []
        self.mouse = None
        self.hero = None
        self.mouse_pos = Vec2(0,0)

    def add_cursor(self, enty):
        Ctrlr.add_enty(self, enty)
        self.cursor = enty

    def add_hero(self, enty):
        Ctrlr.add_enty(self, enty)
        self.hero = enty

    def add_hoop(self, enty):
        Ctrlr.add_enty(self, enty)
        self.hoops.append(enty)
        self.held.append(True)
        self.pressed.append(0)
        self.released.append(0)

    def handle_mouse(self):
        raw_mouse_pos = pygame.mouse.get_pos()
        self.mouse_pos = Vec2(raw_mouse_pos[0], self.flipy(raw_mouse_pos[1]))
        

    def handle_event(self, event):
        '''Respond to event, grabs joystick state'''
        count = len(self.hoops)
        if event.type == pygame.JOYBUTTONDOWN:
            for i in range(count):
                if event.button == i and self.held[i]:
                    self.pressed[i] = self.hoops[i].elapsed_time
        elif event.type == pygame.JOYBUTTONUP:
            for i in range(count):
                if event.button == i and self.held[i]:
                    self.released[i] = self.hoops[i].elapsed_time - self.pressed[i]
                    self.pressed[i] = 0

    def tick(self, delta):
        '''Manipulates the all controlled entities based on inputs and limits'''
        hero_pos = self.hero.get_pos()

        cursor_pos = self.cursor.get_pos()
        next_cursor_pos = cursor_pos.lerp_step(self.mouse_pos, 500*delta)
        self.cursor.set_pos(next_cursor_pos)

        clamped_x = max(150, min(550, next_cursor_pos.x))
        clamped_hero = Vec2(clamped_x, hero_pos.y)

        next_hero_pos = hero_pos.lerp_step(clamped_hero, 500*delta)
        self.hero.set_pos(next_hero_pos)
        count = len(self.hoops)
        for i in range(count):
            target_pos = hero_pos+Vec2(10*i,0)
            if self.released[i] > 0.01:
                self.held[i] = False
                self.released[i] = 0
                speed = self.released[i]
                impulse_mag = max(700, min(750*speed, 1500))
                impulse_dir = Vec2(0,1).rotated(self.hero.heading)
                impulse = impulse_dir.scaled(impulse_mag)
                self.hoops[i].impulse(impulse)
            elif not self.held[i]:
                #flying
                hoop_vel = self.hoops[i].get_body_vel()
                if hoop_vel.y < 0:
                    hoop_pos = self.hoops[i].get_pos()
                    diff = hoop_pos - target_pos
                    
                    if diff.y < 30:
                        if diff.x < 30:
                            self.held[i] = True
                        else:
                            next_hoop_pos = hoop_pos.lerp_step(target_pos, 250*delta)
                            self.hoops[i].set_pos(next_hoop_pos)

            else:
                self.hoops[i].set_pos(target_pos)
        return
