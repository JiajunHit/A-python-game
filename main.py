import pygame
import sys
import traceback
from pygame.locals import *
import myplane
import enemy

pygame.init()
pygame.mixer.init()

bg_size = width, length = 480, 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption('Wing of Fury')

background = pygame.image.load("images/background.png").convert()

# load music
pygame.mixer.music.load("sound/game_music.ogg")
pygame.mixer.music.set_volume(0.2)
bullet_sound = pygame.mixer.Sound("sound/bullet.wav")
bullet_sound.set_volume(0.2)
bomb_sound = pygame.mixer.Sound("sound/use_bomb.wav")
bomb_sound.set_volume(0.2)
supply_sound = pygame.mixer.Sound("sound/supply.wav")
supply_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound("sound/get_bullet.wav")
get_bullet_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound("sound/get_bomb.wav")
get_bomb_sound.set_volume(0.2)
upgrade_sound = pygame.mixer.Sound("sound/upgrade.wav")
upgrade_sound.set_volume(0.2)
enemy3_fly_sound = pygame.mixer.Sound("sound/enemy3_flying.wav")
enemy3_fly_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound("sound/enemy1_down.wav")
enemy1_down_sound.set_volume(0.1)
enemy2_down_sound = pygame.mixer.Sound("sound/enemy2_down.wav")
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound("sound/enemy3_down.wav")
enemy3_down_sound.set_volume(0.5)
me_down_sound = pygame.mixer.Sound("sound/me_down.wav")
me_down_sound.set_volume(0.2)

#
def add_small_enemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)
#
def add_middle_enemies(group1, group2, num):
    for i in range(num):
        e2 = enemy.MidEnemy(bg_size)
        group1.add(e2)
        group2.add(e2)
#
def add_large_enemies(group1, group2, num):
    for i in range(num):
        e3 = enemy.LargeEnemy(bg_size)
        group1.add(e3)
        group2.add(e3)


def main():
    pygame.mixer.music.play(-1)

    # generate my plane
    me = myplane.Myplane(bg_size)

    # generate enemy planes
    enemies = pygame.sprite.Group()

    # generate small enemies
    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies, enemies, 15)
    # generate middle enemies
    middle_enemies = pygame.sprite.Group()
    add_middle_enemies(middle_enemies, enemies, 4)
    # generate large enemies
    large_enemies = pygame.sprite.Group()
    add_large_enemies(large_enemies, enemies, 2)

    clock = pygame.time.Clock()

    # switch the images of my plane, True for image1 False for image2
    switch_image = True
    
    # for delay
    delay = 1000

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit

        # test the keyboard
        key_pressed = pygame.key.get_pressed()

        if key_pressed[K_w] or key_pressed[K_UP]:
            me.moveUp()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            me.moveDown()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            me.moveLeft()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            me.moveRight()

        screen.blit(background,(0,0))

        # draw large enemies
        for each in large_enemies:
            each.move()
            if switch_image:
                screen.blit(each.image1, each.rect)
            else:
                screen.blit(each.image2, each.rect)
            # play the sound when in the large enemy appears
            if each.rect.bottom > - 50:
                enemy3_fly_sound.play()
        # draw middle enemies
        for each in middle_enemies:
            each.move()
            screen.blit(each.image, each.rect)
        # draw small enemies
        for each in small_enemies:
            each.move()
            screen.blit(each.image, each.rect)


        # draw my plane
        if switch_image: 
            screen.blit(me.image1, me.rect)
        else:
            screen.blit(me.image2, me.rect)

        # switch image
        if not(delay % 5):
            switch_image = not switch_image
            
        delay -= 1
        if not delay:
            delay = 100
        pygame.display.flip()

        clock.tick(60)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
