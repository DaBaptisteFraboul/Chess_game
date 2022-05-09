import time
import pygame
import chess_engine
import animation_module

font = pygame.font.Font("assets/Retro Gaming.ttf", 12)
animation = animation_module.Animation("assets/test_animation/Metal_slug/Man_eater_walking.png", "assets/test_animation/Metal_slug/Man_eater_walking.json",15)
spritesheet = pygame.image.load("assets/test_animation/Metal_slug/Man_eater_walking.png")
spritesheet_rect = spritesheet.get_rect()
spritesheet_offset = (10,256)
icon = pygame.image.load("assets/test_animation/Metal_slug/man_eater_icon.png")

animation_rect = pygame.Rect(0,0,48,48)
animation.loop = True
animation.playing = True
animation.scale_animation(256,256)
animation_rect.centerx = (375 - 128)
Ensi_grey= pygame.color.Color((75,75,75))

man_eater_spritesheet = animation_module.Sprite_sheet("assets/test_animation/Metal_slug/Man_eater_walking.png","assets/test_animation/Metal_slug/Man_eater_walking.json")
dataArray = []
for frame in man_eater_spritesheet.data["frames"] :
    square = man_eater_spritesheet.get_sprite_data(frame)
    dataArray.append(square)


def draw_square(screen, index) :

    i = int(index) + 1
    square = dataArray[i]
    x = spritesheet_offset[0] + square[0]
    y = spritesheet_offset[1] + square[1]
    width = square[2]
    height = square[3]
    pygame.draw.rect(screen, (255,0,0), (x,y,width,height), width= 3)


def animation_breakdown_window() :
    running = True
    copyright = font.render('Sprite from Metal Slug 3 by SNK ',True, (255,255,255))
    author = font.render('Baptiste Fraboul - Ensi promo 2023 : ', True, (255,255,255))
    github = font.render('https://github.com/DaBaptisteFraboul', True, (255,255,255))
    window_size = (750,325)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Animation Breakdown - Jury 2022 - E4")
    pygame.display.set_icon(icon)
    previous_time = time.time()
    clock = pygame.time.Clock()
    while running:
        now = time.time()
        dt = now - previous_time
        previous_time = now
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                running = False
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_SPACE :
                    if animation.playing :
                        animation.playing = False
                        break
                    else :
                        animation.playing = True
                if event.key == pygame.K_RIGHT :
                    animation.index += 1
                    animation.index = int(animation.index)
                    if animation.index > 13 :
                        animation.index = 0
                if event.key == pygame.K_LEFT:
                    animation.index -= 1
                    animation.index = int(animation.index)
                    if animation.index < 0:
                        animation.index = 13
        screen.fill(Ensi_grey)


        screen.blit(spritesheet,spritesheet_offset)
        screen.blit(copyright, (10, 10))
        screen.blit(author, (10, 235))
        screen.blit(github,(420, 235))
        animation.display_animation(screen,animation_rect,dt)
        draw_square(screen, animation.index)
        pygame.display.flip()
        clock.tick(60)



animation_breakdown_window()