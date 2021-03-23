import pygame

import pymunk
from pymunk import Vec2d

import os


from ctrlr import Ctrlr, AICtrlr, HumanCtrlr, MouseCtrlr
from enty import Enty
from circenty import CircEnty
from lineenty import LineEnty

ents = []
ctrlrs = []

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def flipy(y):
    """Small hack to convert chipmunk physics to pygame coordinates"""
    return -y + 380


def makeLineEnt(space, name, color, path, pt1, pt2, btype):
    result = LineEnty(name, pygame.Color(color), path)
    result.addCollision(space, pt1, pt2, btype)
    ents.append(result)
    return result

def makeCircleEnt(space, name, color, path, pos, radius, btype):
    result = CircEnty(name, pygame.Color(color), radius, path)
    result.addCollision(space, pos, btype)
    ents.append(result)
    return result

def main():
    pygame.init()
    screen = pygame.display.set_mode((620, 380))
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

    # World
    raw_bg_img = pygame.image.load("bg.jpg")
    bg_img = pygame.transform.scale(
                raw_bg_img, (620,396))

    _ = makeLineEnt(space, "leftWall", "orange", 
        None, (110,30), (110,550), pymunk.Body.STATIC)
    _ = makeLineEnt(space, "rightWall", "orange", 
        None, (610,30), (610,550), pymunk.Body.STATIC)

    # Entities
    aitarget0 = makeCircleEnt(space, "target0", "red", 
        None, (0,300), 10, pymunk.Body.DYNAMIC)
    aitarget1 = makeCircleEnt(space, "target1", "yellow", 
        None, (0,310), 10, pymunk.Body.DYNAMIC)
    aitarget2 = makeCircleEnt(space, "target2", "green", 
        None, (0,320), 10, pymunk.Body.DYNAMIC)
    aitarget3 = makeCircleEnt(space, "target3", "blue", 
        None, (0,330), 10, pymunk.Body.KINEMATIC)
    aitarget4 = makeCircleEnt(space, "target4", "brown", 
        None, (0,340), 10, pymunk.Body.KINEMATIC)

    mouseball = makeCircleEnt(space, "mouse", "white", 
        "hoop.png", (10,10), 40, pymunk.Body.KINEMATIC)
    
    ball0 = makeCircleEnt(space, "ball-r", "red", 
        "hoopred.png", (200+110*0, 320), 50, pymunk.Body.DYNAMIC)
    ball1 = makeCircleEnt(space, "ball-y", "yellow", 
        "hoopyellow.png", (200+110*1, 320), 50, pymunk.Body.DYNAMIC)
    ball2 = makeCircleEnt(space, "ball-g", "green",
        "hoopgreen.png", (200+110*2, 320), 50, pymunk.Body.DYNAMIC)
    ball3 = makeCircleEnt(space, "ball-b", "blue",
        "hoopblue.png", (200+110*3, 320), 50, pymunk.Body.DYNAMIC)
    
    # Controller
    aiCtrlr = AICtrlr([aitarget0,aitarget1,aitarget2,aitarget3,aitarget4])
    ctrlrs.append(aiCtrlr)
    mouseCtrlr = MouseCtrlr([mouseball], flipy)
    ctrlrs.append(mouseCtrlr)
    humanCtrlr = HumanCtrlr([ball0, ball1, ball2, ball3])
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
        font = pygame.font.Font(None, 16)
        line = "Inactive" if paused else "Active"
        text = font.render(line, True, pygame.Color("black"))
        screen.blit(text, (5, 5))

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
