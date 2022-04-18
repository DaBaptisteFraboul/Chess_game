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
        self.clicked = False
        self.animation = animation_module.Animation(spritesheet, data, framerate)
        self.image = self.animation.frames[0]
        self.rect = self.image.get_rect()
        self.set_position(pos_x,pos_y)
        self.animation.index = len(self.animation.frames) - 1

    def set_position(self, x,y):
        self.rect.x, self.rect.y = x, y

    def button_display(self, screen, dt):
        if self.clicked:
            self.animation.playing = True
            self.animation.display_animation(screen, self.rect, dt,False)
            self.clicked = self.animation.playing
        else:
            screen.blit(self.image,self.rect)

    def scale_button(self, x ,y):
        pos_x, pos_y = self.rect.x, self.rect.y
        self.animation.scale_animation(x,y)
        self.image = self.animation.frames[0]
        self.rect = self.image.get_rect(x=pos_x, y=pos_y)


    def click_event(self, mx, my):
        if self.rect.collidepoint(mx, my):
            if not self.clicked :
                self.clicked = True

        return self.clicked


class SwitchButton(Button):
    def __init__(self,pos_x, pos_y,  spritesheet, framerate, pressed):
        """

        :param pos_x:
        :param pos_y:
        :param spritesheet:
        :param framerate:
        :param pressed: Boolean
        """
        super().__init__(pos_x, pos_y,  spritesheet, framerate)
        self.pressed = pressed
        print(self.pressed)
        if self.pressed:
            self.animation.index = len(self.animation.frames) - 1
            self.image = self.animation.frames[0]
        if not self.pressed:
            self.animation.index = 0
            self.image = self.animation.frames[len(self.animation.frames) - 1]

    def click_event(self, mx, my):
        if self.rect.collidepoint(mx, my):
            if not self.clicked:
                self.clicked = True
                if self.pressed :
                    self.animation.index = len(self.animation.frames) - 1
                    self.image = self.animation.frames[0]
                if not self.pressed:
                    self.animation.index = 0
                    self.image = self.animation.frames[len(self.animation.frames) - 1]

                return self.clicked

    def button_display(self, screen, dt):

        if self.clicked:
            if self.pressed :
                self.animation.playing = True
                self.animation.display_animation(screen, self.rect, dt, False)
                if not self.animation.playing :
                    self.clicked = False
                    self.pressed = False
                    return

            if not self.pressed:
                self.animation.playing = True
                self.animation.display_animation(screen, self.rect, dt, True)
                if not self.animation.playing:
                    self.clicked = False
                    self.pressed = True
                    return

        if not self.clicked:
            if self.pressed :
               screen.blit(self.animation.frames[-1], self.rect)
            else :
                screen.blit(self.animation.frames[0], self.rect)