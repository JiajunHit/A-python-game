import pygame
import sys
import traceback
from pygame.locals import *

pygame.init()
pygame.mixer.init()

bg_size = width, length = 480, 700
screen = pygame.display.setmode(bg_size)
pygame.display.set_caption('Wing of Fury')

background = pygame.image.load("image/background.png").convert()

# load music

def main():
    pygame.mixer.music.play(-1)

    clock = pygame.time.clock()

    runnning = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit

        screen.blit(background,(0,0))

        pygame.display.flip()

        clock.tick(60)


if __name__ == "main":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
