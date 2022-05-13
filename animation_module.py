import pygame
import json

class Sprite_sheet():
    """
    Permet de charger l'image correspondant à une frame depuis une sprite sheet
    """

    def __init__(self, spritesheet, animation_data):
        self.filename = spritesheet
        # charge l'image dans self.image:
        self.image_file = pygame.image.load(self.filename)
        # charge le dictionnaire dans self.data
        with open(animation_data) as f:
            self.data = json.load(f)
        f.close()
        self.frames_list = []

    def get_sprite(self, x, y, w, h):
        """
        Cette méthode renvoie l'image de la sprite sheet en fonction des coordonées x, y, w,h

        """
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(self.image_file, (0, 0), (x, y, w, h))
        return sprite



    def get_sprite_data(self, name):
        '''
        cette méthode permet d'obtenir les coordonnées de l'image dans la sprite sheet
        à partir du nom de la frame
        '''
        sprite_data = self.data["frames"][name]["frame"]
        x, y, w, h = sprite_data["x"], sprite_data["y"], sprite_data["w"], sprite_data["h"]
        return x, y, w, h

    def image(self, name):
        """
        cette fonction permet d'obtenir l'image coresspondant au nom de la frame

        """
        x, y, w, h = self.get_sprite_data(name)
        image = self.get_sprite(x, y, w, h)
        return image

    def get_frames_arrray(self):
        for frame in self.data["frames"]:
            frame_image = self.image(frame)
            self.frames_list.append(frame_image)

        return self.frames_list

class Animation:
    def __init__(self, spritesheet, json, animation_framerate):
        self.sprites_loader = Sprite_sheet(spritesheet, json)
        self.frames = self.sprites_loader.get_frames_arrray()
        self.framerate = animation_framerate
        self.increment = (self.framerate/60)
        self.index = 0
        self.playing = False
        self.loop = False

    def scale_animation(self, x, y):
        for i in range(len(self.frames)) :
            image = pygame.transform.scale(self.frames[i], (y,x))
            self.frames[i] = image

    def set_framerate(self, framerate):
        self.framerate = framerate

    def draw_frame(self, screen, rect):
        screen.blit(self.frames[int(self.index)], rect)

    def update_index_forward(self, dt):
        self.index += self.increment * (dt * 60)
        if self.index > len(self.frames) - 1 :
            self.index = 0
            if not self.loop :
                self.playing = False

    def update_index_backwardd(self, dt):
        self.index -= self.increment * (dt * 60)
        if self.index < 0:
            self.index = len(self.frames) - 1
            if not self.loop:
                self.playing = False

    def display_animation(self, screen, rect, dt, forward = True) :
        """
        On appelle cette méthode dans la boucle display
        """
        if self.playing :
            if forward :
                self.draw_frame(screen, rect)
                self.update_index_forward(dt)

            if not forward :
                self.draw_frame(screen, rect)
                self.update_index_backwardd(dt)
        else :
            self.draw_frame(screen, rect)


