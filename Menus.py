import pygame

import Gui
import chess_globals_variable
import constants
import chess_engine
import sys
import time
import animation_module
from Gui import *

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

# Fonts


class Menu:
    '''
    Cette classe définie le principe des menus et les éléments récurents que l'on va retrouver dedans
    la boucle du menu est contenue non pas dans une fonction mais dans une méthdode.

    Chaque menu serra une classe enfant qui héritera de cette méthode :
    Je me crée un workflow de programmation.

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
        self.right_clicking = False
        self.app_running = True
        # Framerate independence
        self.previous_time = time.time()



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
         # nécessaire pour réutiliser plusieures fois le menu
        self.is_running = True
        while self.is_running :
            self.now =time.time()
            self.dt = self.now - self.previous_time
            self.previous_time = self.now
            self.events()
            self.update()
            self.display()
            self.clock.tick(60)
            if constants.quit :
                break
        return

class MainMenu(Menu) :
    """
    Overrider les fonctions spécifiques au Main Menu
    """
    def __init__(self, screen) :
        super().__init__(screen)
        print("Pause initialized")
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

class PauseMenu(Menu):
    def __init__(self, screen, pause_bg):
        super().__init__(screen)
        self.font = pygame.font.Font("assets/Retro Gaming.ttf",24)
        self.Pause_title = self.font.render("Pause Title", 150,200)
        self.color = pygame.Color(125,125,135,a = 125)
        self.surface = pygame.Surface((300,500), flags=pygame.SRCALPHA)
        self.surface.fill(self.color)
        self.surface.set_alpha(200)
        self.pause_bg = pause_bg
        self.trainer_animation = animation_module.Animation("assets/test_animation/trainer_sheet.png",
                                                            "assets/test_animation/trainer_sheet.json",
                                                            5)
        self.image = pygame.image.load('assets/board/export/pieces/03/white_king.png')
        self.mask = self.image.get_masks()

        self.trainer_animation.playing = True
        self.trainer_animation.loop = True
        self.animation_rect = pygame.Rect(100,100,500,500)
        self.quit_button = Button(40,60,"assets/GUI/button_pressed.png", 12)
        self.quit_button.scale_button(64,128)


    def handle_keyboard_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.type == pygame.QUIT :
                self.is_running = False
                constants.quit_game()
            if event.key == pygame.K_ESCAPE:
                self.is_running = False



            if event.key == pygame.K_w:
                print("pressed during pause")


    def events(self):
        for event in pygame.event.get() :
            if event.type == pygame.QUIT:
                constants.quit = True
            self.handle_keyboard_events(event)
            self.handle_click_event(event)

    def update(self):
        pass

    def handle_click_event(self, event):
        self.mx, self.my = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN :
            if event.button == 1 :
                print("click at {}".format((self.mx, self.my)))
                if self.quit_button.click_event(self.mx, self.my) :
                    pass

    def display(self):

        self.screen.blit(self.pause_bg, (0,0))
        self.quit_button.button_display(self.screen, self.dt)
        self.trainer_animation.display_animation(self.screen, self.animation_rect, self.dt)
        self.screen.blit(self.Pause_title, (100,300))
        pygame.display.flip()



class ChessGame(Menu) :
    def __init__(self, screen, player_color ):
        super().__init__(screen)
        self.reset_button = Button(592,164, "assets/GUI/button_pressed.png",17)
        self.reset_button.scale_button(32,64)
        self.quit_boutton = Button(652,8,"assets/GUI/Quit_button.png",17)
        self.quit_boutton.scale_button(44,40)
        self.player_color = player_color
        self.board = chess_engine.ChessBoard()
        self.board.set_starting_position()
        self.color_switch = Gui.SwitchButton(588,72, "assets/GUI/Black_switch.png",24,True)
        self.color_switch.scale_button(44,104)
        self.left_ui = pygame.image.load('assets/board/export/Left_UI.png')
        self.left_ui = pygame.transform.scale(self.left_ui, (64,768))
        self.right_ui = pygame.image.load('assets/board/export/Right_Ui.png')
        self.right_ui = pygame.transform.scale(self.right_ui, (128,768))
        self.screen_ui = pygame.image.load('assets/board/export/Screen_UI.png')
        self.screen_ui = pygame.transform.scale(self.screen_ui,(512, 128))
        self.board_ui = pygame.image.load('assets/board/export/chessboard_tex.png')
        self.board_ui = pygame.transform.scale(self.board_ui, (512,512))
        self.right_ui_pos = (576,0)
        self.god_mod = False

        self.Valid_moves = self.board.get_Valid_moves(self.board.colour_to_play)
        self.move_made = False

        self.player_clicks = []
        self.selected_case = ()
        self.computer_move = None
        self.pause_bg = None

        self.pause = PauseMenu(self.screen, self.pause_bg)
        self.endgame_menu = EndgameMenu(self.screen)

        # variable used to avoid to recalculate moves every frames

    def is_inside_board (self, x, y) :
        """
        Cette méthode permet de vérifier si le les coordonées x et y sont bien dans l'échiquier par
        rapport à l'UI de l'application
        :param x:
        :param y:
        :return:
        """
        if 64 < x < 576 and 128 < y < 640 :
            return True
        else :
            return False

    def update(self):
        rerun = False
        if self.board.checkmate or self.board.pat:
            if self.board.checkmate:
                if self.board.colour_to_play == self.player_color:
                    rerun = self.endgame_menu.player_lost = True

                self.endgame_menu.run()
                self.board.set_starting_position()
                print(self.board.board)

                print("Chekmate" + self.board.colour_to_play + " have lost the game")
            if self.board.pat:
                print("Pat - Partie Nulle-")
        if rerun :
            self.board.set_starting_position()
            self.Valid_moves = self.board.get_Valid_moves(self.board.colour_to_play)
    def handle_keyboard_events(self, event):

        if event.type == pygame.QUIT :
            chess_globals_variable.is_running = False
            constants.quit = True
            self.running = False
            sys.exit()
        if event.type == pygame.KEYDOWN and self.board.colour_to_play == self.player_color:
            if event.key == pygame.K_SPACE :
                for moves_in_LOG in self.board.move_LOG :
                    print(moves_in_LOG.get_notation())

            if event.key == pygame.K_v :
                print(chess_globals_variable.test_value)

            if event.key == pygame.K_x :
                chess_globals_variable.change_value()

            if event.key == pygame.K_m :
                self.board.set_starting_position()

            if event.key == pygame.K_a :
                self.board.Undo_Move(self.player_color)
                if self.god_mod :
                    self.board.next_color()
                self.Valid_moves= self.board.get_Valid_moves(self.board.colour_to_play)

            if event.key == pygame.K_b :
                self.board.side = 'white'

            if event.key == pygame.K_n :
                self.board.side = 'black'

            if event.key == pygame.K_s :
                fen = self.board.get_FEN()
                print(self.board.stockfish.get_board_visual())

            if event.key == pygame.K_w :
                if self.god_mod :
                    self.god_mod = False
                else :
                    self.god_mod = True
            if event.key == pygame.K_z :
                fen = self.board.get_FEN()
                print(fen)

            if event.key == pygame.K_f :
                print("f is pressed")
                fen = self.board.get_FEN()
                self.computer_move = self.board.do_best_move(fen)

            if event.key == pygame.K_b :
                print(self.board.board)

            if event.key == pygame.K_p :
                pygame.image.save(self.screen,"pause_screen.png")
                self.pause_bg = pygame.image.load("pause_screen.png")
                self.pause = PauseMenu(self.screen, self.pause_bg)
                self.pause.is_running = True
                self.pause.run()
                print(self.is_running)




    def handle_click_event(self, event):
        """
        gestion des clics de la souris
        """
        self.right_clicking = False
        self.mx, self.my = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # clic droit détecté
            # on vérifie que le click est bien sur le board de l'échiquier
            if self.reset_button.click_event(self.mx, self.my) :
                print("reset button")
                if self.color_switch.pressed :
                    self.player_color = 'black'
                else :
                    self.player_color = 'white'
                self.board.set_starting_position()
                self.Valid_moves = self.board.get_Valid_moves(self.board.colour_to_play)
                self.selected_case = ()
            if self.quit_boutton.click_event(self.mx, self.my) :
                print("Click Quit")

            if self.color_switch.click_event(self.mx, self.my):
                if self.board.side == 'white':
                    self.board.side = 'black'
                    return
                else :
                    self.board.side = 'white'


            if self.is_inside_board(self.mx, self.my) and self.board.colour_to_play == self.player_color:
                if event.button == 1:
                    location = ((self.my - 128) // 64,
                                (
                                            self.mx - 64) // 64)  # on récupère la position du clic sur le board (attention il faut inverser c et r)
                    if self.board.side == 'white':
                        row = location[0]
                        col = location[1]
                    if self.board.side == 'black':
                        row = constants.turn_board[location[0]]
                        col = constants.turn_board[location[1]]
                    # player selected the same case // cancel command
                    if self.selected_case == (row, col):
                        self.selected_case = ()  # deselec
                        self.player_clicks = []
                        print("Cancel Move")
                    else:
                        self.selected_case = (row, col)
                        self.player_clicks.append(self.selected_case)
                    if len(self.player_clicks) == 2:  # nous sommes après le deuxième clic
                        if self.board.get_piece_colour(self.player_clicks[0]) == self.board.colour_to_play:
                            move = chess_engine.Move(self.player_clicks[0], self.player_clicks[1], self.board.board)
                            #if self.board.get_piece_type(self.player_clicks[0]) == 'king' and \
                                    #self.player_clicks[0][1] - self.player_clicks[1][1] != 1:
                               # print(self.player_clicks[1][1] - self.player_clicks[0][1])
                                #print("roque generated from click")
                                #move.is_roque = True
                            if move in self.Valid_moves:
                                self.board.Make_Move(move)
                                self.move_made = True
                                self.player_clicks = []  # deselect
                                self.selected_case = ()
                            if self.board.ongoing_promotion:
                                self.board.draw_board(self.screen)
                                self.board.draw_pieces(self.screen)
                                promotion_square = (
                                self.board.move_LOG[-1].end_row * 64 + constants.board_offset[1],
                                self.board.move_LOG[-1].end_col * 64 + constants.board_offset[0])
                                self.board.set_promotion_menu(self.screen, promotion_square)
                            else:
                                self.player_clicks = []  # deselect
                                self.selected_case = ()
                        else:
                            self.player_clicks = []  # deselect
                            self.selected_case = ()
                if self.move_made:
                    # while god_mode, u skip opponent turn
                    if not self.god_mod:
                        self.board.next_color()
                    self.Valid_moves = self.board.get_Valid_moves(self.board.colour_to_play)
                    self.move_made = False


    def display(self):
        """
        Gère l'affichage des éléments à l'écran, notez bien que l'ordre des méthodes correspond à l'ordre des calques :
        arrière plan => premier plan
        """
        self.screen.fill(constants.default_color)
        self.screen.blit(pygame.image.load("assets/board/export/Application_bg.png"),(0,0))
        self.screen.blit(self.right_ui, self.right_ui_pos)
        self.screen.blit(self.left_ui, (0,0))
        self.screen.blit(self.screen_ui, (64,0))
        self.screen.blit(self.screen_ui, (64,640))
        self.board.draw_board(self.screen)


        self.color_switch.button_display(self.screen, self.dt)
        self.board.draw_pieces(self.screen)
        self.reset_button.button_display(self.screen, self.dt)
        self.quit_boutton.button_display(self.screen, self.dt)
        if self.player_clicks != []:
            self.board.draw_moves(self.screen, self.Valid_moves, self.player_clicks[0])
            # On mettra ici le déclencheement de l'animation de victoire et du menu rejouer.
        if self.selected_case:
            if self.board.board[self.selected_case[0]][self.selected_case[1]] != 'EmptySquare':

                self.board.draw_outline(self.selected_case[0], self.selected_case[1], self.screen)
                self.board.draw_single_piece(self.screen, self.selected_case[1], self.selected_case[0])

        pygame.display.flip()

    def events(self):
        if self.board.colour_to_play != self.player_color :
            print("computer is playing")
            fen = self.board.get_FEN()
            self.computer_move = self.board.do_best_move(fen)
            print(self.board.stockfish.get_board_visual())

        for events in pygame.event.get():
            self.handle_keyboard_events(events)
            self.handle_click_event(events)

            if events.type == pygame.QUIT:
                self.is_running = False
                break
        if not self.computer_move :
            pass
        else:
            self.board.Make_Move(self.computer_move)
            self.board.next_color()
            self.computer_move = None
            self.move_made = False
            self.Valid_moves = self.board.get_Valid_moves(self.board.colour_to_play)





class MainOptions(Menu):
    def __init__(self, screen):
        super().__init__(screen)


class PauseOptionsMenu(Menu):
    def __init__(self, screen):
        super().__init__(screen)

class EndgameMenu(Menu):
    def __init__(self, screen):
        super().__init__(screen)
        self.player_lost = None

    def handle_keyboard_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.is_running = False
                return True

    def handle_click_event(self, event):
        pass

    def update(self):
        pass


    def display(self):
        if self.player_lost :
            self.screen.fill((178,20,20,120))
        else :
            self.screen.fill((20,20,178,120))
        pygame.display.flip()

    def run(self):
        self.is_running = True
        while self.is_running :
            self.events()
            self.update()
            self.display()
            self.clock.tick(60)
            if constants.quit :
                break
class CreditsMenu(Menu):
    def __init__(self, screen):
        super().__init__(screen)

class TitleMenu(Menu):
    def __init__(self, screen):
        super().__init__(screen)






