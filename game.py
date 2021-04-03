from entyline import EntyLine
from entycircle import EntyCircle
from enty import Enty
from ctrlrai import AICtrlr
from ctrlr import Ctrlr, HumanCtrlr, MouseCtrlr
from cnphy.body import Body
from cnphy.space import Space
from cnphy.vec2d import Vec2d

import pygame
import os

# Physics collision types
COLLTYPE_DEFAULT = 0
COLLTYPE_PAWN = 1
COLLTYPE_TARGET = 2


ents = []
controllers = []
SAMPLERATE = 44100
if os.name == 'posix':
    SAMPLERATE = 8000
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def flipy(y):
    """Small hack to convert chipmunk physics to pygame coordinates"""
    return -y + 380


def makeLineEnt(space, name, color, path, pt1, pt2, bodtype, coltype=COLLTYPE_DEFAULT):
    result = EntyLine(name, pygame.Color(color), path)
    result.add_collision(space, pt1, pt2, bodtype, coltype)
    ents.append(result)
    return result


def makeCircleEnt(space, name, color, path, pos, radius, bodtype, coltype=COLLTYPE_DEFAULT):
    result = EntyCircle(name, pygame.Color(color), radius, path)
    result.add_collision(space, pos, bodtype, coltype)
    ents.append(result)
    return result


def pawn_target_func(arbiter, _space, _data):
    """Simple callback that increases the radius of circles touching the mouse"""
    shape1, shape2 = arbiter.shapes
    cnshape1 = shape1.cnshape
    cnshape2 = shape2.cnshape
    bodtype1 = shape1.body.body_type
    bodtype2 = shape2.body.body_type
    id1 = cnshape1.owner.name[-1]
    id2 = cnshape2.owner.name[-1]
    if(id1 == id2):
        if bodtype1 == Body.DYNAMIC:
            cnshape2.owner.attach = cnshape1.owner
        elif bodtype2 == Body.DYNAMIC:
            cnshape1.owner.attach = cnshape2.owner
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
    space = Space()
    space.gravity = 0.0, -981.0

    space.add_collision_handler(COLLTYPE_PAWN, COLLTYPE_TARGET, pawn_target_func)

    # World
    raw_bg_img = pygame.image.load("bg.jpg")
    bg_img = pygame.transform.scale(
        raw_bg_img, (620, 396))

    _ = makeLineEnt(space, "leftWall", "orange",
                    None, Vec2d(110, 30), Vec2d(110, 550), 
                    Body.STATIC)
    _ = makeLineEnt(space, "rightWall", "orange",
                    None, Vec2d(610, 30), Vec2d(610, 550), 
                    Body.STATIC)

    # Entities
    aitarget0 = makeCircleEnt(space, "target0", "red",
                              "birdred.png", Vec2d(0, 0), 10,
                              Body.KINEMATIC, COLLTYPE_TARGET)
    aitarget1 = makeCircleEnt(space, "target1", "yellow",
                              "birdyellow.png", Vec2d(0, 0), 10,
                              Body.KINEMATIC, COLLTYPE_TARGET)
    aitarget2 = makeCircleEnt(space, "target2", "green",
                              "birdgreen.png", Vec2d(0, 0), 10,
                              Body.KINEMATIC, COLLTYPE_TARGET)
    aitarget3 = makeCircleEnt(space, "target3", "blue",
                              "birdblue.png", Vec2d(0, 0), 10,
                              Body.KINEMATIC, COLLTYPE_TARGET)
    aitarget4 = makeCircleEnt(space, "target4", "brown",
                              "birdbrown.png", Vec2d(0, 0), 10,
                              Body.KINEMATIC, COLLTYPE_TARGET)

    mouseball = makeCircleEnt(space, "mouse", "white",
                              "hoop.png", Vec2d(10, 10), 40, 
                              Body.KINEMATIC)

    pawn0 = makeCircleEnt(space, "pawn0", "red",
                          "hoopred.png", Vec2d(200+110*0, 320), 50,
                          Body.DYNAMIC, COLLTYPE_PAWN)
    pawn1 = makeCircleEnt(space, "pawn1", "yellow",
                          "hoopyellow.png", Vec2d(200+110*1, 320), 50,
                          Body.DYNAMIC, COLLTYPE_PAWN)
    pawn2 = makeCircleEnt(space, "pawn2", "green",
                          "hoopgreen.png", Vec2d(200+110*2, 320), 50,
                          Body.DYNAMIC, COLLTYPE_PAWN)
    pawn3 = makeCircleEnt(space, "pawn3", "blue",
                          "hoopblue.png", Vec2d(200+110*3, 320), 50,
                          Body.DYNAMIC, COLLTYPE_PAWN)

    # Controller
    ai_controller = AICtrlr([aitarget0, aitarget1, aitarget2, aitarget3, aitarget4])
    controllers.append(ai_controller)
    mouse_controller = MouseCtrlr([mouseball], flipy)
    controllers.append(mouse_controller)
    human_controller = HumanCtrlr([pawn0, pawn1, pawn2, pawn3], SAMPLERATE)
    controllers.append(human_controller)

    # GameState
    run_physics = True
    paused = False

    last_secs = -1
    # Loop
    while running:

        mouse_controller.handle_event(0)
        for event in pygame.event.get():
            if (event.type == pygame.JOYAXISMOTION or
                event.type == pygame.JOYHATMOTION or
                event.type == pygame.JOYBUTTONDOWN or
                    event.type == pygame.JOYBUTTONUP):
                if event.joy == 0:
                    human_controller.handle_event(event)
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
            delta = 1.0 / 60.0
            steps = 1
            for _ in range(steps):
                for ent in ents:
                    ent.tick(delta)
                for ctrlr in controllers:
                    ctrlr.tick(delta)
                space.step(delta)

        # Draw stuff
        screen.blit(bg_img, (0, 0))

        # Display some text
        smfont = pygame.font.Font(None, 16)
        line = "Inactive" if paused else "Active"
        text = smfont.render(line, True, pygame.Color("gray"))
        screen.blit(text, (5, 5))
        bigfont = pygame.font.Font(None, 32)
        scoreline = "Score " + str(ai_controller.score)
        scoretext = bigfont.render(scoreline, True, pygame.Color("black"))
        screen.blit(scoretext, (5, 370))

        secs = round(mouseball.elapsed_time)
        if secs != last_secs:
            last_secs = secs
            if (secs % 10 == 0):
                print(str(secs)+", Score:"+str(ai_controller.score))
        timeline = "Time " + str(secs)
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
    main()
