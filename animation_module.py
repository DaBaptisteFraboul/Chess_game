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
        cette fonction permet d'obtenir l'image coresspondant au nom de la framef
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
    def __init__(self, spritesheet, json):
        self.sprites_loader = Sprite_sheet(spritesheet, json)
        self.animation = self.sprites_loader.get_frames_arrray()
        self.index = 0

    def draw_frame(self, screen):
        screen.blit(self.animation[self.index], (0,0))

    def update_index(self):
        self.index += 1
        if self.index > len(self.animation) :
            self.index = 0




def run_animation() :
    spriteheet = Animation("assets/test_animation/trainer_sheet.png", "assets/test_animation/trainer_sheet.json")
    running = True
    window = pygame.display.set_mode((256,256))
    clock = pygame.time.Clock()

    while running :

       spriteheet.sprites_loader.get_frames_arrray()
       pygame.display.flip()
       clock.get_fps()
       for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                running = False
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_SPACE :
                    print("update")
                    spriteheet.update_index()

       window.fill('black')
       window.blit(spriteheet.animation[spriteheet.index], (0,0))
run_animation()



