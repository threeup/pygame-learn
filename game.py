import pygame

import pymunk
from pymunk import Vec2d


from ctrlr import Ctrlr
from enty import Enty

X, Y = 0, 1


def flipy(y):
    """Small hack to convert chipmunk physics to pygame coordinates"""
    return -y + 380

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
    space.gravity = 0.0, -900.0

    # Entities
    hero = Enty("hero", pygame.Color("black"))
    mouse = Enty("mouse", pygame.Color("purple"))
    player0 = Ctrlr(hero)


    # GameState
    run_physics = True
    paused = False

    # Loop
    while running:

        for event in pygame.event.get():
            if (event.type == pygame.JOYAXISMOTION or
                event.type == pygame.JOYHATMOTION or
                event.type == pygame.JOYBUTTONDOWN or
                    event.type == pygame.JOYBUTTONUP):
                if event.joy == 0:
                    player0.handle_event(event)
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
                player0.tick(dt)
                hero.tick(dt)
                space.step(dt)

        # Update mouse
        p = pygame.mouse.get_pos()
        mouse.set_pos(p[X], flipy(p[Y]))

        # Draw stuff
        screen.fill(player0.col)

        # Display some text
        font = pygame.font.Font(None, 48)
        line = "Greetings"+str(not paused)
        text = font.render(line, True, pygame.Color("black"))
        screen.blit(text, (5, 5))


        # Draw ents
        hero_pos = hero.get_draw_pos(flipy)
        pygame.draw.circle(screen, hero.color, hero_pos, int(hero.radius), 12)
        mouse_pos = mouse.get_draw_pos(flipy)
        pygame.draw.circle(screen, mouse.color, mouse_pos, int(mouse.radius), 5)

        # Flip screen
        pygame.display.flip()
        clock.tick(50)
        pygame.display.set_caption("fps: " + str(clock.get_fps()))


if __name__ == "__main__":
    doprof = 0
    if not doprof:
        main()
