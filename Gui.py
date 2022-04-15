import time

import pygame
import animation_module

class Button:
    def __init__(self,pos_x, pos_y,  spritesheet, framerate):
        '''
        Initialiser le button avec sa position dans l'espace et son image
        et ses animations
        '''
        data = spritesheet.replace("png","json")
        self.pressed = False
        self.animation = animation_module.Animation(spritesheet, data, framerate)
        self.image = self.animation.frames[0]
        self.rect = self.image.get_rect()
        self.set_position(pos_x,pos_y)

    def set_position(self, x,y):
        self.rect.x, self.rect.y = x, y

    def button_display(self, screen, dt):
        if self.pressed:
            self.animation.playing = True
            self.animation.display_animation(screen, self.rect, dt)
            self.pressed = self.animation.playing
        else:
            screen.blit(self.image,self.rect)

    def scale_button(self, x ,y):
        pos_x, pos_y = self.rect.x, self.rect.y
        self.animation.scale_animation(x,y)
        self.image = self.animation.frames[0]
        self.rect = self.image.get_rect(x=pos_x, y=pos_y)

    def clicked(self):
        "Méthode à appeler lorsque le bouton est pressé"
        print("Pressed button")

    def click_event(self, mx, my):
        if self.rect.collidepoint(mx, my):
            if not self.pressed :
                self.pressed = True
        return self.pressed





"""win = pygame.display.set_mode((200,200))
button = Button(10,10,"assets/GUI/button_pressed.png",12)
button.scale_button(64,128)
button.set_position(12,50)
running = True
previous_time = time.time()
while running :
    now = time.time()
    dt = now - previous_time
    previous_time = now
    mx, my = pygame.mouse.get_pos()
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN :
            button.click_event(mx, my)
    win.fill("black")
    button.button_display(win, dt)

    pygame.display.flip()
"""