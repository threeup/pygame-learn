''' holds Ctrlr and RefCtrlr class '''
import pygame
import random

from ctrlr import Ctrlr
from world import World
from entycircle import EntyCircle
from cnphy.body import Body
from cnphy.vec2 import Vec2


class RefCtrlr(Ctrlr):
    '''
    A class which manages game state and rules
    '''

    def __init__(self, world):
        # invoking the __init__ of the parent class
        Ctrlr.__init__(self)
        self.world = world
        self.difficulty = 0
        self.human = None
        self.mouse = None
        self.agent = None
    
    def tick(self, _delta):
        '''manages stuff'''
        self.difficulty += 1

    def add_human(self, ctrlr):
        ''' attach human '''
        self.human = ctrlr

    def add_mouse(self, ctrlr):
        ''' attach mouse '''
        self.mouse = ctrlr

    def add_agent(self, ctrlr):
        ''' attach agent '''
        self.agent = ctrlr

    def make_circle(self, name, color, path, pos, radius, bodtype, coltype):
        '''Create a circle entity and attach to physics simulation'''
        result = EntyCircle(name, pygame.Color(color), radius, path)
        space = self.world.space
        result.add_collision(space, pos, bodtype, coltype)
        self.world.ents.append(result)
        return result

    def make_agent_ent(self, idx):
        ''' Create a circle bird ent and attach to ai controller '''
        if idx == 0:
            name = "target0"
            color = "red"
        elif idx == 1:
            name = "target1"
            color = "yellow"
        elif idx == 2:
            name = "target2"
            color = "green"
        elif idx == 3:
            name = "target3"
            color = "blue"
        else:
            name = "target4"
            color = "brown"
        filename = "bird"+color+".png"
        ent = self.make_circle(name, color,
                               filename, Vec2(0, 0), 10,
                               Body.KINEMATIC, World.COLLTYPE_TARGET)
        self.agent.add_enty(ent)

    def make_human_ent(self, idx):
        ''' Create a circle hoop ent and attach to human controller '''
        if idx == 0:
            name = "pawn0"
            color = "red"
        elif idx == 1:
            name = "pawn1"
            color = "yellow"
        elif idx == 2:
            name = "pawn2"
            color = "green"
        elif idx == 3:
            name = "pawn3"
            color = "blue"
        else:
            return
        filename = "hoop"+color+".png"
        ent = self.make_circle(name, color,
                               filename, Vec2(200+110*idx, 320), 50,
                               Body.DYNAMIC, World.COLLTYPE_PAWN)
        self.human.add_hoop(ent)

    def make_basic(self):
        ''' make some fundamentals '''
        ent = self.make_circle("cursor", "white",
                               "hoop.png", Vec2(10, 200), 40,
                               Body.KINEMATIC, World.COLLTYPE_CURSOR)
        self.human.add_cursor(ent)

        ent = self.make_circle("hero", "purple",
                               "hoop.png", Vec2(350, 40), 20,
                               Body.KINEMATIC, World.COLLTYPE_DEFAULT)
        self.human.add_hero(ent)

    def make_good(self, count):
        ''' make a pair of hoops and birds of the same color '''
        values = []
        for _ in range(count):
            if len(values) == 0:
                values = [0,1,2,3]
            color = random.choice(values)
            values.remove(color)
            self.make_agent_ent(color)
            self.make_human_ent(color)

    def make_noise(self, count):
        ''' make birds of garbage color '''
        values = []
        for _ in range(count):
            if len(values) == 0:
                values = [4,5,6,7]
            color = random.choices(values)
            self.make_agent_ent(color)
    
