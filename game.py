''' holds a bunch of stuff '''
import os
import pygame

from world import World
from entyline import EntyLine
from ctrlrref import RefCtrlr
from ctrlragent import AgentCtrlr
from ctrlrhuman import HumanCtrlr
from cnphy.body import Body
from cnphy.space import Space
from cnphy.vec2 import Vec2


controllers = []
SAMPLERATE = 44100
if os.name == 'posix':
    SAMPLERATE = 8000
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def flipy(value):
    '''Small hack to convert chipmunk physics to pygame coordinates'''
    return -value + 380


def make_line(world, name, color, path, pt1, pt2, bodtype, coltype):
    '''Create a line segment entity and attach to physics simulation'''
    space = world.space
    result = EntyLine(name, pygame.Color(color), path)
    result.add_collision(space, pt1, pt2, bodtype, coltype)
    world.ents.append(result)
    return result


def main():
    '''main'''
    pygame.mixer.pre_init(SAMPLERATE, -16, 2, 64)
    pygame.mixer.init()
    pygame.init()
    screen = pygame.display.set_mode((780, 420))
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

    world = World(space)

    # World
    raw_bg_img = pygame.image.load("bg.jpg")
    bg_img = pygame.transform.scale(
        raw_bg_img, (780, 420))

    make_line(world, "leftWall", "orange",
              None, Vec2(110, 30), Vec2(110, 550),
              Body.STATIC, World.COLLTYPE_DEFAULT)
    make_line(world, "rightWall", "orange",
              None, Vec2(610, 30), Vec2(610, 550),
              Body.STATIC, World.COLLTYPE_DEFAULT)

    # Controller
    human = HumanCtrlr(flipy)
    controllers.append(human)
    agent = AgentCtrlr()
    controllers.append(agent)
    ref = RefCtrlr(world)
    ref.add_human(human)
    ref.add_agent(agent)
    controllers.append(ref)

    # start
    ref.make_basic()
    ref.make_good(2)
    ref.make_noise(4)
    paused = False
    last_secs = -1

    # Loop
    while running:
        human.handle_mouse()
        for event in pygame.event.get():
            if (event.type == pygame.JOYAXISMOTION or
                event.type == pygame.JOYHATMOTION or
                event.type == pygame.JOYBUTTONDOWN or
                    event.type == pygame.JOYBUTTONUP):
                if event.joy == 0:
                    human.handle_event(event)
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.ACTIVEEVENT:
                paused = bool(event.gain == 0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                paused = True
            elif event.type == pygame.MOUSEBUTTONUP:
                paused = False

        # Update
        delta = 1.0 / 60.0
        steps = 1
        for _ in range(steps):
            if world.run_physics:
                world.tick(delta)
                space.step(delta)
            for ctrlr in controllers:
                ctrlr.tick(delta)

        # Draw stuff
        screen.blit(bg_img, (0, 0))

        # Display some text
        smfont = pygame.font.Font(None, 16)
        line = "Inactive" if paused else "Active"
        text = smfont.render(line, True, pygame.Color("gray"))
        screen.blit(text, (5, 5))
        bigfont = pygame.font.Font(None, 32)
        scoreline = "Score " + str(agent.score)
        scoretext = bigfont.render(scoreline, True, pygame.Color("black"))
        screen.blit(scoretext, (5, 370))

        secs = round(world.elapsed_time)
        if secs != last_secs:
            last_secs = secs
            if secs % 10 == 0:
                print(str(secs)+", Score:"+str(agent.score))
        timeline = "Time " + str(secs)
        timetext = bigfont.render(timeline, True, pygame.Color("black"))
        screen.blit(timetext, (400, 370))

        # Draw ents
        world.draw(screen, flipy)

        # Flip screen
        pygame.display.flip()
        clock.tick(50)
        pygame.display.set_caption("fps: " + str(clock.get_fps()))


if __name__ == "__main__":
    main()
