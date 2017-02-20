import pygame
import sys
import traceback
from pygame.locals import *
import myplane
import enemy
import bullet

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

    # generate bullets
    bullet1 = []
    bullet1_index = 0
    BULLET1_NUM = 4
    for i in range (BULLET1_NUM):
        bullet1.append(bullet.Bullet1(me.rect.midtop))

    # index of the images when crash
    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0
    me_destroy_index = 0

    # switch the images of my plane, True for image1 False for image2
    switch_image = True
    
    # for delay
    delay = 100
    
    clock = pygame.time.Clock()

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

        # shoot the bullets
        if not(delay % 10):
            bullet1[bullet1_index].reset(me.rect.midtop)
            bullet1_index = (bullet1_index + 1) % BULLET1_NUM

        # test if the bullets have hitted the enemies
        for  b in bullet1:
            if b.active:
                b.move()
                screen.blit(b.image, b.rect)
                enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                if enemy_hit:
                    b.active = False
                    for e in enemy_hit:
                        e.active = False

        # draw large enemies
        for each in large_enemies:
            if each.active:
                each.move()
                if switch_image:
                    screen.blit(each.image1, each.rect)
                else:
                    screen.blit(each.image2, each.rect)
                # play the sound when in the large enemy appears
                if each.rect.bottom == -50:
                    enemy3_fly_sound.play(-1)
            else:
                # destroy the large plane
                if not(delay % 3):
                    enemy3_fly_sound.stop()
                    # play the destroy sound
                    if e3_destroy_index == 0:
                        enemy3_down_sound.play()
                    # switch the destroy images and reset
                    screen.blit(each.destroy_images[e3_destroy_index], each.rect)
                    e3_destroy_index = (e3_destroy_index + 1) % 6
                    # reset
                    if e3_destroy_index == 0:
                        each.reset()

        # draw middle enemies
        for each in middle_enemies:
            if each.active:
                each.move()
                screen.blit(each.image, each.rect)
            else:
                # destroy the middle plane
                if not(delay % 3):
                    # play the destroy sound
                    if e2_destroy_index == 0:
                        enemy2_down_sound.play()
                    screen.blit(each.destroy_images[e2_destroy_index], each.rect)
                    e2_destroy_index = (e2_destroy_index + 1) % 4
                    if e2_destroy_index == 0:
                        each.reset()

        # draw small enemies
        for each in small_enemies:
            if each.active:
                each.move()
                screen.blit(each.image, each.rect)
            else:
                # destroy the small plane
                if not(delay % 3):
                    # play the destroy sound
                    if e1_destroy_index == 0:
                        enemy1_down_sound.play()
                    screen.blit(each.destroy_images[e1_destroy_index], each.rect)
                    e1_destroy_index = (e1_destroy_index + 1) % 4
                    if e1_destroy_index == 0:
                        each.reset()

        # collide test if my plane is crashed
        enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
        if enemies_down:
            # me.active = False
            for each in enemies_down:
                each.active = False

        # draw my plane
        if me.active:
            if switch_image: 
                screen.blit(me.image1, me.rect)
            else:
                screen.blit(me.image2, me.rect)
        else:
            # destroy my plane
            if not(delay % 3):
                # play the destroy sound
                if me_destroy_index == 0:
                    me_down_sound.play()
                screen.blit(me.destroy_images[me_destroy_index], me.rect)
                me_destroy_index = (me_destroy_index + 1) % 4
                if me_destroy_index == 0:
                    each.reset()


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
