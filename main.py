import pygame
import sys
import traceback
import myplane
import enemy
import bullet
import supply
from pygame.locals import *
from random import *

pygame.init()
pygame.mixer.init()

bg_size = width, height = 480, 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption('Wing of Fury')

background = pygame.image.load("images/background.png").convert()

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

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

def increase_speed(target, inc):
    for each in target:
        each.speed += inc

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

    # generate super bullets
    bullet2 = []
    bullet2_index = 0
    BULLET2_NUM = 8
    for i in range (BULLET2_NUM // 2):
        bullet2.append(bullet.Bullet2((me.rect.centerx-33, me.rect.centery)))
        bullet2.append(bullet.Bullet2((me.rect.centerx+30, me.rect.centery)))

    # statistic the scores
    score = 0
    score_font = pygame.font.Font("font/font.ttf", 36)

    # pause or resume the game
    pause = False
    pause_nor_image = pygame.image.load("images/pause_nor.png").convert_alpha()
    pause_pressed_image = pygame.image.load("images/pause_pressed.png").convert_alpha()
    resume_nor_image = pygame.image.load("images/resume_nor.png").convert_alpha()
    resume_pressed_image = pygame.image.load("images/resume_pressed.png").convert_alpha()
    pause_rect = pause_nor_image.get_rect()
    pause_rect.left, pause_rect.top = width - pause_rect.width - 10, 10
    pause_image = pause_nor_image

    # set levels
    level = 1

    # bomb
    bomb_image = pygame.image.load("images/bomb.png").convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_font = pygame.font.Font("font/font.ttf", 48)
    bomb_num = 3

    # grant a supply each 30 seconds
    bullet_supply = supply.Bullet_supply(bg_size)
    bomb_supply = supply.Bomb_supply(bg_size)
    SUPPLY_TIMER = USEREVENT
    pygame.time.set_timer(SUPPLY_TIMER, 30 * 1000)

    # super bullet timer
    DOUBLE_BULLET_TIMER = USEREVENT + 1

    # sign whether or not to use the super bullet
    is_double_bullet = False

    # abort the invincible status timer
    INVINCIBLE_TIMER = USEREVENT + 2

    # life amount
    life_image = pygame.image.load("images/life.png").convert_alpha()
    life_rect = life_image.get_rect()
    life_num = 3

    # the game over screen
    gameover_font = pygame.font.Font("font/font.ttf", 48)
    again_image = pygame.image.load("images/again.png").convert_alpha()
    again_rect = again_image.get_rect()
    gameover_image = pygame.image.load("images/gameover.png").convert_alpha()
    gameover_rect = gameover_image.get_rect()
    
    # to prevent the record file opened again and again
    recorded = False

    # switch the images of my plane, True for image1 False for image2
    switch_image = True
    
    # for delay
    delay = 100
    
    clock = pygame.time.Clock()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit
                pygame.quit()
            
            # test whether or not user clicks the pause button
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1 and pause_rect.collidepoint(event.pos):
                    pause = not pause
                    if pause:
                        pygame.time.set_timer(SUPPLY_TIMER, 0)
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        pygame.time.set_timer(SUPPLY_TIMER, 30 * 1000)
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()

            # the whether or not the mouse is on the pause button
            elif event.type == MOUSEMOTION:
                if pause_rect.collidepoint(event.pos):
                    if pause:
                        pause_image = resume_pressed_image
                    else:
                        pause_image = pause_pressed_image
                else:
                    if pause:
                        pause_image = resume_nor_image
                    else:
                        pause_image = pause_nor_image

            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if bomb_num:
                        bomb_num -= 1
                        bomb_sound.play()
                        for each in enemies:
                            if each.rect.bottom > 0:
                                each.active = False

            elif event.type == SUPPLY_TIMER:
                supply_sound.play()
                if choice([True, False]):
                    bomb_supply.reset()
                else:
                    bullet_supply.reset()

            elif event.type == DOUBLE_BULLET_TIMER:
               is_double_bullet = False
               pygame.time.set_timer(DOUBLE_BULLET_TIMER, 0)

            elif event.type == INVINCIBLE_TIMER:
                me.invincible = False
                pygame.time.set_timer(INVINCIBLE_TIMER, 0)
        
        # increase the game difficulty level based on the score
        if level == 1 and score > 500:
            level = 2
            upgrade_sound.play()
            # add three small enenies and two middle enemies and one large enemie
            add_small_enemies(small_enemies, enemies, 3)
            add_middle_enemies(middle_enemies, enemies, 2)
            add_large_enemies(large_enemies, enemies, 1)
            # increase the speed of small_enemies
            increase_speed(small_enemies, 1)
        elif level == 2 and score > 1000:
            level = 3
            upgrade_sound.play()
            # add three small enenies and two middle enemies and one large enemie
            add_small_enemies(small_enemies, enemies, 5)
            add_middle_enemies(middle_enemies, enemies, 3)
            add_large_enemies(large_enemies, enemies, 2)
            # increase the speed of small_enemies
            increase_speed(small_enemies, 1)
            increase_speed(middle_enemies, 1)
        elif level == 3 and score > 2000:
            level = 4
            upgrade_sound.play()
            # add three small enenies and two middle enemies and one large enemie
            add_small_enemies(small_enemies, enemies, 3)
            add_middle_enemies(middle_enemies, enemies, 2)
            add_large_enemies(large_enemies, enemies, 1)
            # increase the speed of small_enemies
            increase_speed(small_enemies, 1)
            increase_speed(middle_enemies, 1)
        elif level == 4 and score > 4000:
            level = 5
            upgrade_sound.play()
            # add three small enenies and two middle enemies and one large enemie
            add_small_enemies(small_enemies, enemies, 3)
            add_middle_enemies(middle_enemies, enemies, 2)
            add_large_enemies(large_enemies, enemies, 1)
            # increase the speed of small_enemies
            increase_speed(small_enemies, 1)
            increase_speed(middle_enemies, 1)

        screen.blit(background,(0,0))

        if life_num and not pause:
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

            # provide the bomb supply
            if bomb_supply.active:
                bomb_supply.move()
                screen.blit(bomb_supply.image, bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply, me):
                    get_bomb_sound.play()
                    if bomb_num < 3:
                        bomb_num += 1
                    bomb_supply.active = False

            # provide the bullet supply
            if bullet_supply.active:
                bullet_supply.move()
                screen.blit(bullet_supply.image, bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply, me):
                    get_bullet_sound.play()
                    is_double_bullet = True
                    pygame.time.set_timer(DOUBLE_BULLET_TIMER, 20 * 1000)
                    bullet_supply.active = False

            # shoot the bullets
            if not(delay % 10):
                bullet_sound.play()
                if is_double_bullet:
                    bullets = bullet2
                    bullets[bullet2_index].reset((me.rect.centerx-33, me.rect.centery))
                    bullets[bullet2_index + 1].reset((me.rect.centerx+30, me.rect.centery))
                    bullet2_index = (bullet2_index + 2) % BULLET2_NUM
                else:
                    bullets = bullet1
                    bullet1[bullet1_index].reset(me.rect.midtop)
                    bullet1_index = (bullet1_index + 1) % BULLET1_NUM

            # test if the bullets have hitted the enemies
            for  b in bullets:
                if b.active:
                    b.move()
                    screen.blit(b.image, b.rect)
                    enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                    if enemy_hit:
                        b.active = False
                        for e in enemy_hit:
                            if e in middle_enemies or e in large_enemies:
                                e.energy -= 1
                                e.hit = True
                                if e.energy == 0:
                                    e.active = False
                            else:
                                e.active = False

            # draw large enemies
            for each in large_enemies:
                if each.active:
                    each.move()
                    each.draw_plane(switch_image, screen)

                    # draw life bar
                    pygame.draw.line(screen, BLACK, \
                                (each.rect.left, each.rect.top - 5), \
                                (each.rect.right, each.rect.top - 5), \
                                2)
                    energy_remain = each.energy / enemy.LargeEnemy.energy
                    if energy_remain < 0.2:
                        energy_color = RED
                    else:
                        energy_color = GREEN
                    pygame.draw.line(screen, energy_color, \
                                (each.rect.left, each.rect.top - 5), \
                                (each.rect.left + energy_remain * each.rect.width, each.rect.top - 5), \
                                2)

                    # play the sound when in the large enemy appears
                    if each.rect.bottom == -50:
                        each.fly_sound.play(-1)

                else:
                    # destroy the large plane
                    if not(delay % 3):
                        # play the destroy sound
                        if each.destroy_index == 0:
                            each.down_sound.play()
                        # switch the destroy images and reset
                        screen.blit(each.destroy_images[each.destroy_index], each.rect)
                        each.destroy_index = (each.destroy_index + 1) % 6
                        # reset
                        if each.destroy_index == 0:
                            score += 100
                            each.reset()

            # draw middle enemies
            for each in middle_enemies:
                if each.active:
                    each.move()
                    each.draw_plane(screen)

                    # draw life bar
                    pygame.draw.line(screen, BLACK, \
                                (each.rect.left, each.rect.top - 5), \
                                (each.rect.right, each.rect.top - 5), \
                                2)
                    energy_remain = each.energy / enemy.MidEnemy.energy
                    if energy_remain < 0.2:
                        energy_color = RED
                    else:
                        energy_color = GREEN
                    pygame.draw.line(screen, energy_color, \
                                (each.rect.left, each.rect.top - 5), \
                                (each.rect.left + energy_remain * each.rect.width, each.rect.top - 5), \
                                2)

                else:
                    # destroy the middle plane
                    if not(delay % 3):
                        # play the destroy sound
                        if each.destroy_index == 0:
                            each.down_sound.play()
                        screen.blit(each.destroy_images[each.destroy_index], each.rect)
                        each.destroy_index = (each.destroy_index + 1) % 4
                        if each.destroy_index == 0:
                            score += 60
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
                        if each.destroy_index == 0:
                            each.down_sound.play()
                        screen.blit(each.destroy_images[each.destroy_index], each.rect)
                        each.destroy_index = (each.destroy_index + 1) % 4
                        if each.destroy_index == 0:
                            score += 10
                            each.reset()

            # collide test if my plane is crashed
            enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
            if enemies_down and not me.invincible:
                me.active = False
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
                    if me.destroy_index == 0:
                        me.down_sound.play()
                    screen.blit(me.destroy_images[me.destroy_index], me.rect)
                    me.destroy_index = (me.destroy_index + 1) % 4
                    if me.destroy_index == 0:
                        life_num -= 1
                        me.reset()
                        pygame.time.set_timer(INVINCIBLE_TIMER, 3 * 1000)

            # show the bombs remian at the left bottom corner
            bomb_text = bomb_font.render("x %d" % bomb_num, True, WHITE)
            text_rect = bomb_text.get_rect()
            screen.blit(bomb_image, (10, height -10 -bomb_rect.height))
            screen.blit(bomb_text, (20 + bomb_rect.width, height -5 -text_rect.height))

            # show the lives remian at the right bottom corner
            if life_num:
                for i in range(life_num):
                    screen.blit(life_image, \
                                (width-10-(i+1)*life_rect.width, height-5-life_rect.height))
            # drwa the score
            score_text = score_font.render("Score : %s" % str(score), True, WHITE)
            screen.blit(score_text, (10, 5))

        # when game over
        elif life_num == 0:
            # stop the background music
            pygame.mixer.music.stop()
            # stop all the sound
            pygame.mixer.stop()
            # stop the supply
            pygame.time.set_timer(SUPPLY_TIMER, 0)

            if not recorded:
                recorded = True

                # read the best score in histroy
                with open("record.txt", "r") as f:
                    record_score = int(f.read())

                # if the score is better than the record score save the score
                if score > record_score:
                    with open("record.txt", "w") as f:
                        f.write(str(score))

            # draw the game over screen
            record_score_text = score_font.render("BEST : %d" % record_score, True, WHITE)
            screen.blit(record_score_text, (50, 50))

            gameover_text1 = gameover_font.render("YOUR SCORE", True, WHITE)
            gameover_text1_rect = gameover_text1.get_rect()
            gameover_text1_rect.left, gameover_text1_rect.top = \
                        (width - gameover_text1_rect.width) // 2, 180
            screen.blit(gameover_text1, gameover_text1_rect)

            gameover_text2 = gameover_font.render(str(score), True, WHITE)
            gameover_text2_rect = gameover_text2.get_rect()
            gameover_text2_rect.left, gameover_text2_rect.top = \
                        (width - gameover_text2_rect.width) // 2, gameover_text1_rect.bottom + 10
            screen.blit(gameover_text2, gameover_text2_rect)

            again_rect.left, again_rect.top = \
                        (width - again_rect.width) // 2, \
                        gameover_text2_rect.bottom + 50
            screen.blit(again_image, again_rect)

            gameover_rect.left, gameover_rect.top = \
                        (width - gameover_rect.width) // 2, \
                        again_rect.bottom + 10
            screen.blit(gameover_image, gameover_rect)
            
            # test the mouse
            # the left button is clicked
            if pygame.mouse.get_pressed()[0]:
                # get the position of the mouse
                pos = pygame.mouse.get_pos()

                # user click PLAY AGAIN
                if again_rect.left < pos[0] < again_rect.right and \
                            again_rect.top < pos[1] < again_rect.bottom:
                    main()
                # user click GAME OVER
                if gameover_rect.left < pos[0] < gameover_rect.right and \
                            gameover_rect.top < pos[1] < gameover_rect.bottom:
                    pygame.quit()
                    sys.exit()


        # draw the pause button
        screen.blit(pause_image, pause_rect)

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
