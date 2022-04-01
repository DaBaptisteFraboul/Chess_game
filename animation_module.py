import time
import pygame
import json

class SpritesLoader():
    """
    Permet de charger l'image correspondant à une frame depuis une sprite sheet et un fichier json contenant les
    données de l'animation
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
        Cette fonction permet d'obtenir l'image coresspondant au nom de la frame
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
    """
    Cette classe contient la liste des frames associées à une animation ainsi que des méthodes d'appels
    """
    def __init__(self, spritesheet, json):
        self.sprites_loader = SpritesLoader(spritesheet, json)
        self.frames = self.sprites_loader.get_frames_arrray()
        self.index = 0

    def draw_animation(self, screen):
        screen.blit(self.frames[int(self.index)], (0, 0))

    def update_index(self, delta_time):

        self.index += (60/24) * delta_time
        if self.index > len(self.frames) :
            self.index = 0




def run_animation() :
    previous_time = time.time()

    spriteheet = Animation("assets/test_animation/trainer_sheet.png", "assets/test_animation/trainer_sheet.json")
    running = True
    window = pygame.display.set_mode((256,256))
    clock = pygame.time.Clock()

    while running :
        now = time.time()
        dt = now - previous_time
        previous_time = now
        spriteheet.sprites_loader.get_frames_arrray()
        pygame.display.flip()
        clock.get_fps()
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                running = False
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_SPACE :
                    i = 0
                    while i < 300000 :
                        i += 1
                        print(i)
        spriteheet.update_index(dt)
        print(clock.get_fps())
        clock.tick(60)
        window.fill('black')
        spriteheet.draw_animation(window)
run_animation()



