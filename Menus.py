import pygame
import constants
import chess_engine

"""
Une c'est une fonction avec une boucle While runnin avec sa propre variable running
pour avoir un systeme de menu il faut créer chaque boucle de menu dans sa propre fonction.

Pour appeler un menu on appelle sa fonction /

Pour arreter le menu plusieur options :
    - On appelle un nouveau menu dans la boucle qui va suspendre la boucle du menu précédent (un menu pause est une bonne option)
    - On met la variable running de la boucle du menu en valeur False
    
Un système de menu est donc un emboitement de boucles avec géré avec des variables running

L'idée est de stocker chaque menu dans une variable au lancement du programme et de l'appeler au moment nécessaire avec 
la méthode run()
"""

class Menu:
    '''
    Cette classe définie le principe des menus et les élémentes récurents que l'on va retrouver dedans
    la boucle du menu est contenu non pas dans une focntion mais dans une méthdode.

    Chaque menu serrra une classe enfant qui héritera de cette méthode :
    Je me créé un workflow de programation.

    Pour qu ele menu fonctionne, il doit avoir en variable les ressource techniques qui lui permet de fonctionner :
    - ressources graphiques : sprites / système d'animation etc.
    - ressources sonores :
    - on utilise les variable que dans la boucle bien fermée
    '''
    def __init__(self, screen) :
        self.is_running = True
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.mx, self.my = pygame.mouse.get_pos()


    def handle_click_event(self, event):
        print("mouse method no set for menu")
        self.is_running = False

    def handle_keyboard_events(self, event):
        print("keyboard method not set for menu ")
        self.is_running = False

    def update(self):
        print("update methode not set for menu")

    def events(self):
        for events in pygame.event.get():
            self.handle_click_event(events)
            self.handle_keyboard_events(events)
            if events.type == pygame.QUIT:
                self.is_running = False
                break

    def display(self):
        print("display method not set for menu")
        pygame.display.flip()

    def run(self):
        self.is_running = True # nécessaire pour réutiliser plusieures fois le menu
        while self.is_running :
            self.events()
            self.update()
            self.display()



class MainMenu(Menu) :
    """
    Overrider les fonctions spécifiques au Main Menu

    """
    def __init__(self, screen) :
        super().__init__(screen)
        # importer les ressources spécifiques au Main Menu (assets, sons, pygame.Rect) depuis les constants
        # e.g. self.ressource = constant.ressource

    def handle_click_event(self, event):
        """
        Gestion de la souris
        :param event:
        :return:
        """

        if event.type == pygame.MOUSEBUTTONDOWN :
            if event.button == 1 : #rightclick
                print("Right click ! at position {}".format((self.mx, self.my)))
                # do some shit


    def handle_keyboard_events(self, event):
        """
        Gestion du clavier

        :param event:
        :return:
        """
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_SPACE :
                print('Space Key pressed!')
                #Do some shit

class ChessGame(Menu) :
    def __init__(self, screen):
        super().__init__(screen)

class MainOptions(Menu):
    def __init__(self, screen):
        super().__init__(screen)

class PauseMenu(Menu):
    def __init__(self, screen):
        super().__init__(screen)

class PauseOptionsMenu(Menu):
    def __init__(self, screen):
        super().__init__(screen)

class EndgameMenu(Menu):
    def __init__(self, screen):
        super().__init__(screen)

class CreditsMenu(Menu):
    def __init__(self, screen):
        super().__init__(screen)

class TitleMenu(Menu):
    def __init__(self, screen):
        super().__init__(screen)






