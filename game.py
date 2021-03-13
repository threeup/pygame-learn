import pygame

import pymunk
from pymunk import Vec2d

X, Y = 0, 1

def flipy(y):
    """Small hack to convert chipmunk physics to pygame coordinates"""
    return -y + 600

def main():

    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()
    running = True

    ### Joystick stuff
    pygame.joystick.init()
    joystick_count = pygame.joystick.get_count()

    joysticks = [pygame.joystick.Joystick(x) for x in range(joystick_count)]
    for j in range(joystick_count):
        joysticks[j].init()

    ### Physics stuff
    space = pymunk.Space()
    space.gravity = 0.0, -900.0

    
    ### Mouse
    mouse_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    mouse_shape = pymunk.Circle(mouse_body, 30, (0, 0))
    mouse_shape.collision_type = 1
    space.add(mouse_body, mouse_shape)

    colc = pygame.Color("cyan")
    colg = pygame.Color("green")
    col = colc

    run_physics = True
    
    evtype = 0
    while running:
        moving = False
        ## _pygame.h PGPOST_EVENTBEGIN
        ## pygame-stubs/constants.pyi 
        ## https://github.com/davidsiaw/SDL2/blob/master/include/SDL_events.h
        for j in range(joystick_count):
            joystick = joysticks[j]
            buttons = joystick.get_numbuttons()
            for i in range(buttons):
                button = joystick.get_button(i)
                if button:
                    print(button,i)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                col = colc
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_g:
                col = colg
            elif event.type == pygame.MOUSEBUTTONUP:
                moving = True
            elif event.type == pygame.JOYAXISMOTION:
                moving = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                moving = True
            elif event.type == pygame.MOUSEMOTION:
                moving = True
            elif event.type == pygame.KEYUP: 
                moving = True
            elif event.type == pygame.KEYDOWN:
                moving = True
            elif event.type == pygame.ACTIVEEVENT:
                moving = True
            elif event.type == 2304: ##clipboardupdate
                moving = True
            else:
                print("s")
                print(event)
                evtype = event.type

        p = pygame.mouse.get_pos()
        mouse_pos = Vec2d(p[X], flipy(p[Y]))
        mouse_body.position = mouse_pos

        
        ### Update physics  
        if run_physics:
            dt = 1.0 / 60.0
            for _ in range(1):
                space.step(dt)

        ### Draw stuff
        screen.fill(col)

        # Display some text
        font = pygame.font.Font(None, 48)
        line = "Greetings"+str(moving)
        text = font.render(line, True, pygame.Color("black"))
        screen.blit(text, (5, 5))
        line = "Ev"+str(evtype)
        text = font.render(line, True, pygame.Color("black"))
        screen.blit(text, (5, 60))

        r = mouse_shape.radius
        v = mouse_shape.body.position
        p = int(v.x), int(flipy(v.y))
        pygame.draw.circle(screen, pygame.Color("blue"), p, int(r), 2)

        
        ### Flip screen
        pygame.display.flip()
        clock.tick(50)
        pygame.display.set_caption("fps: " + str(clock.get_fps()))


if __name__ == "__main__":
    doprof = 0
    if not doprof:
        main()

