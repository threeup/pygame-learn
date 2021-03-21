import pygame

import pymunk
from pymunk import Vec2d


from ctrlr import Ctrlr, AICtrlr, HumanCtrlr, MouseCtrlr
from enty import Enty

ents = []
ctrlrs = []


def flipy(y):
    """Small hack to convert chipmunk physics to pygame coordinates"""
    return -y + 380

def makeEnt(name, color):
    result = Enty(name, pygame.Color(color))
    ents.append(result)
    return result

def makeCircleEnt(space, name, color, pos, btype):
    result = makeEnt(name, color)
    result.addCircleCollision(space, pos, btype)
    if(pos[0] > 400):
        result.debug = True
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


    # Entities
    #aiball = makeCircleEnt("hero", "white", space, pymunk.Body.KINEMATIC)
    mouseball = makeCircleEnt(space, "mouse", "white", (10,10), pymunk.Body.KINEMATIC)
    
    ball0 = makeCircleEnt(space, "ball-r", "red", (100+110*0, 320), pymunk.Body.DYNAMIC)
    ball1 = makeCircleEnt(space, "ball-y", "yellow", (100+110*1, 320),pymunk.Body.DYNAMIC)
    ball2 = makeCircleEnt(space, "ball-g", "green", (100+110*2, 320),pymunk.Body.DYNAMIC)
    ball3 = makeCircleEnt(space, "ball-b", "blue", (100+110*3, 320), pymunk.Body.DYNAMIC)
    
    # Controller
    #aiCtrlr = AICtrlr([aiball])
    #ctrlrs.append(aiCtrlr)
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
        screen.fill(pygame.Color("cyan"))

        # Display some text
        font = pygame.font.Font(None, 48)
        line = "Active"+str(not paused)
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
