from entyline import EntyLine
from entycircle import EntyCircle
from enty import Enty
from ctrlrai import AICtrlr
from ctrlr import Ctrlr, HumanCtrlr, MouseCtrlr
import pygame

import pymunk
from pymunk import Vec2d

import os

# Physics collision types
COLLTYPE_DEFAULT = 0
COLLTYPE_PAWN = 1
COLLTYPE_TARGET = 2


ents = []
ctrlrs = []
SAMPLERATE = 44100
if os.name == 'posix':
    SAMPLERATE = 4000
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def flipy(y):
    """Small hack to convert chipmunk physics to pygame coordinates"""
    return -y + 380


def makeLineEnt(space, name, color, path, pt1, pt2, bodtype, coltype=COLLTYPE_DEFAULT):
    result = EntyLine(name, pygame.Color(color), path)
    result.addCollision(space, pt1, pt2, bodtype, coltype)
    ents.append(result)
    return result


def makeCircleEnt(space, name, color, path, pos, radius, bodtype, coltype=COLLTYPE_DEFAULT):
    result = EntyCircle(name, pygame.Color(color), radius, path)
    result.addCollision(space, pos, bodtype, coltype)
    ents.append(result)
    return result


def pawn_target_func(arbiter, space, data):
    """Simple callback that increases the radius of circles touching the mouse"""
    s1, s2 = arbiter.shapes
    bodtype1 = s1.body.body_type
    bodtype2 = s2.body.body_type
    id1 = s1.owner.name[-1]
    id2 = s2.owner.name[-1]
    if(id1 == id2):
        if bodtype1 == pymunk.Body.DYNAMIC:
            s2.owner.attach = s1.owner
        elif bodtype2 == pymunk.Body.DYNAMIC:
            s1.owner.attach = s2.owner
        return False
    return True


def main():
    pygame.mixer.pre_init(SAMPLERATE, -16, 2, 64)
    pygame.mixer.init()
    pygame.init()
    screen = pygame.display.set_mode((620, 400))
    clock = pygame.time.Clock()
    running = True

    # Joystick stuff
    pygame.joystick.init()
    joystick_count = pygame.joystick.get_count()

    joysticks = [pygame.joystick.Joystick(x) for x in range(joystick_count)]
    for j in range(joystick_count):
        joysticks[j].init()

    # Physics stuff
    space = pymunk.Space()
    space.gravity = 0.0, -981.0

    space.add_collision_handler(
        COLLTYPE_PAWN, COLLTYPE_TARGET
    ).pre_solve = pawn_target_func

    # World
    raw_bg_img = pygame.image.load("bg.jpg")
    bg_img = pygame.transform.scale(
        raw_bg_img, (620, 396))

    _ = makeLineEnt(space, "leftWall", "orange",
                    None, (110, 30), (110, 550), 
                    pymunk.Body.STATIC)
    _ = makeLineEnt(space, "rightWall", "orange",
                    None, (610, 30), (610, 550), 
                    pymunk.Body.STATIC)

    # Entities
    aitarget0 = makeCircleEnt(space, "target0", "red",
                              None, (0, 0), 10,
                              pymunk.Body.DYNAMIC, COLLTYPE_TARGET)
    aitarget1 = makeCircleEnt(space, "target1", "yellow",
                              None, (0, 0), 10,
                              pymunk.Body.DYNAMIC, COLLTYPE_TARGET)
    aitarget2 = makeCircleEnt(space, "target2", "green",
                              None, (0, 0), 10,
                              pymunk.Body.DYNAMIC, COLLTYPE_TARGET)
    aitarget3 = makeCircleEnt(space, "target3", "blue",
                              None, (0, 0), 10,
                              pymunk.Body.KINEMATIC, COLLTYPE_TARGET)
    aitarget4 = makeCircleEnt(space, "target4", "brown",
                              None, (0, 0), 10,
                              pymunk.Body.KINEMATIC, COLLTYPE_TARGET)

    mouseball = makeCircleEnt(space, "mouse", "white",
                              "hoop.png", (10, 10), 40, 
                              pymunk.Body.KINEMATIC)

    pawn0 = makeCircleEnt(space, "pawn0", "red",
                          "hoopred.png", (200+110*0, 320), 50,
                          pymunk.Body.DYNAMIC, COLLTYPE_PAWN)
    pawn1 = makeCircleEnt(space, "pawn1", "yellow",
                          "hoopyellow.png", (200+110*1, 320), 50,
                          pymunk.Body.DYNAMIC, COLLTYPE_PAWN)
    pawn2 = makeCircleEnt(space, "pawn2", "green",
                          "hoopgreen.png", (200+110*2, 320), 50,
                          pymunk.Body.DYNAMIC, COLLTYPE_PAWN)
    pawn3 = makeCircleEnt(space, "pawn3", "blue",
                          "hoopblue.png", (200+110*3, 320), 50,
                          pymunk.Body.DYNAMIC, COLLTYPE_PAWN)

    # Controller
    aiCtrlr = AICtrlr([aitarget0, aitarget1, aitarget2, aitarget3, aitarget4])
    ctrlrs.append(aiCtrlr)
    mouseCtrlr = MouseCtrlr([mouseball], flipy)
    ctrlrs.append(mouseCtrlr)
    humanCtrlr = HumanCtrlr([pawn0, pawn1, pawn2, pawn3], SAMPLERATE)
    ctrlrs.append(humanCtrlr)

    # GameState
    run_physics = True
    paused = False

    # Loop
    while running:

        mouseCtrlr.handle_event(0)
        for event in pygame.event.get():
            if (event.type == pygame.JOYAXISMOTION or
                event.type == pygame.JOYHATMOTION or
                event.type == pygame.JOYBUTTONDOWN or
                    event.type == pygame.JOYBUTTONUP):
                if event.joy == 0:
                    humanCtrlr.handle_event(event)
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.ACTIVEEVENT:
                if event.gain == 0:
                    paused = True
                else:
                    paused = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                paused = True
            elif event.type == pygame.MOUSEBUTTONUP:
                paused = False

        # Update physics
        if run_physics:
            dt = 1.0 / 60.0
            steps = 1
            for _ in range(steps):
                for ent in ents:
                    ent.tick(dt)
                for ctrlr in ctrlrs:
                    ctrlr.tick(dt)
                space.step(dt)

        # Draw stuff
        screen.blit(bg_img, (0, 0))

        # Display some text
        smfont = pygame.font.Font(None, 16)
        line = "Inactive" if paused else "Active"
        text = smfont.render(line, True, pygame.Color("gray"))
        screen.blit(text, (5, 5))
        bigfont = pygame.font.Font(None, 32)
        scoreline = "Score " + str(aiCtrlr.score)
        scoretext = bigfont.render(scoreline, True, pygame.Color("black"))
        screen.blit(scoretext, (5, 370))

        timeline = "Time " + str(round(mouseball.elapsed_time))
        timetext = bigfont.render(timeline, True, pygame.Color("black"))
        screen.blit(timetext, (400, 370))

        # Draw ents
        for ent in ents:
            ent.draw(screen, flipy)

        # Flip screen
        pygame.display.flip()
        clock.tick(50)
        pygame.display.set_caption("fps: " + str(clock.get_fps()))


if __name__ == "__main__":
    doprof = 0
    if not doprof:
        main()
