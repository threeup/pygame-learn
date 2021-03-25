import pygame

import numpy as np
import os

SAMPLERATE = 4000

def make_tone(self, freq=1000, volume=10000, length=1):
    
    num_steps = int(length*SAMPLERATE)
    intro = int(length*SAMPLERATE*0.2)
    s = []

    for n in range(num_steps):
        value = np.sin(n * freq * (6.28318/SAMPLERATE) * length)*volume
        if n < intro:
            ease = n/intro
            s.append([value*ease, value*ease])
        elif (num_steps-n) < intro:
            ease = (num_steps-n)/intro
            s.append([value*ease, value*ease])
        else:
            s.append([value, value])
    buffer = np.array(s)
    return pygame.sndarray.make_sound(buffer.astype(np.int16))

def main():
    pygame.mixer.pre_init(SAMPLERATE, -16, 2, 64)
    pygame.mixer.init()
    pygame.init()
    _ = pygame.display.set_mode((620, 400))
    print(pygame.mixer.get_init())
    pygame.mixer.music.load("hendrik.wav")
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        continue
    
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue
    
    tone = make_tone(400)
    print(tone.get_volume())
    
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            else:
                tone.play()
        pygame.display.flip()
        pygame.display.set_caption("fps: ")

if __name__ == "__main__":
    doprof = 0
    if not doprof:
        main()
