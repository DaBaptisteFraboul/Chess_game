# -*- coding: utf-8 -*-

import math
import pygame
import chess_engine
import sys, time
import constants

#Taille finale de l'application (704,768), taille de l'échiquier (512,512)
class Game :
    """
    Cette classe contient l'affichage de la partie d'échecs
    Je dois encore clarifier comment le faire proprement, pour l'instant il s'agit également de la gestion de l'application



    """
    def __init__(self):
        # classic pygame stuff
        self.window_size = (704,768)
        self.window = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Chess game!")
        self.running = True
        self.clock = pygame.time.Clock()

        self.board = chess_engine.ChessBoard()
        self.board.set_starting_position()

        # gestion des moves légaux
        self.Valid_moves = self.board.get_Valid_moves(self.board.colour_to_play)
        self.move_made = False #variable used to avoid to recalculate moves every frames

        # Mouse related variables

        self.right_clicking = False
        self.mx , self.my = pygame.mouse.get_pos()
        self.player_clicks = []
        self.selected_case = ()

        pygame.mouse.set_cursor(pygame.cursors.diamond)

        # for debugging purpose :

        self.god_mod = False

        # chess Ai

        self.computer_move = None


    def final_screen(self):
        """
        Unused To replace, doesnt work, I must understand to display font in pygame before trying to implement it into
        my application ofc.

        :return:
        """
        running = True
        window = pygame.display.set_mode(self.window_size)
        message_rect = pygame.Rect((10,256),(64, 256))
        if self.board.pat :
            text = 'Stalemate, no one won the game'
        if self.board.checkmate :
            winner = self.board.opponent_colour(self.board.colour_to_play)
            text = winner + " have won the game by checkmate"
        message = constants.Arial_font.render(text, True, 'Red', (0, 0, 0))
        while running :
            for event in pygame.event.get():
                if event.type == pygame.K_ESCAPE :
                    sys.exit()
            window.blit(message,message_rect)

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
    '''
    Permet la gestion dela boucle d'events, tout ce qui est input du joueur est géré ici
    '''
    def handle_click_event(self, event):
        """
        gestion des clics de la souris
        """

        if event.type == pygame.MOUSEBUTTONDOWN:
            # clic droit détecté
            #on vérifie que le click est bien sur le board de l'échiquier
            if self.is_inside_board(self.mx, self.my) :
                if event.button == 1:
                    location = ((self.my - 128)// 64,
                                (self.mx - 64)// 64)  # on récupère la position du clic sur le board (attention il faut inverser c et r)
                    row = location[0]
                    col = location[1]
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
                            print()
                            if self.board.get_piece_type(self.player_clicks[0]) == 'king' and\
                                self.player_clicks[0][1] - self.player_clicks[1][1] != 1 :
                                    move.is_roque = True

                            if move in self.Valid_moves :
                                if move.is_pawn_charge :
                                    print('charge')
                                self.board.Make_Move(move)
                                self.move_made = True
                                self.player_clicks = []  # deselect
                                self.selected_case = ()

                            if self.board.ongoing_promotion:
                                self.board.draw_board(self.window)
                                self.board.draw_pieces(self.window)
                                promotion_square = (self.board.move_LOG[-1].end_row * 64 + constants.board_offset[1],
                                                    self.board.move_LOG[-1].end_col * 64 + constants.board_offset[0])
                                self.board.set_promotion_menu(self.window, promotion_square)

                            else:
                                self.player_clicks = []  # deselect
                                self.selected_case = ()


                        else:
                            self.player_clicks = []  # deselect
                            self.selected_case = ()

                if self.move_made:
                    # while god_mode, u skip opponent turn
                    if not self.god_mod :
                        self.board.next_color()
                    self.Valid_moves = self.board.get_Valid_moves(self.board.colour_to_play)

                    self.move_made = False
            else :
                print("Outside gameboard")


    def events(self):

        self.right_clicking = False
        self.mx, self.my = pygame.mouse.get_pos()
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                self.running = False
                sys.exit()

            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_SPACE :
                    for moves_in_LOG in self.board.move_LOG :
                        print(moves_in_LOG.get_notation())

                if event.key == pygame.K_a :
                    self.board.Undo_Move()
                    if self.god_mod :
                        self.board.next_color()
                    self.Valid_moves= self.board.get_Valid_moves(self.board.colour_to_play)

                if event.key == pygame.K_b :
                    self.board.get_Valid_moves(self.board.colour_to_play)

                if event.key == pygame.K_w :
                    if self.god_mod :
                        self.god_mod = False
                    else :
                        self.god_mod = True

                if event.key == pygame.K_x :
                    for moves in self.Valid_moves:
                        print(moves.is_roque)

                if event.key == pygame.K_f :
                    fen = self.board.get_FEN()
                    self.computer_move = ai.do_best_move(fen, self.board.board)



            if not self.computer_move :
                self.handle_click_event(event)
            else :
                self.board.Make_Move(self.computer_move)
                self.board.next_color()
                self.computer_move = None

    '''
    La boucle update nous servira à faire des mise à jour automatique en fonction des changement d'état
    '''
    def update(self):
        # On coupe la promotion dans une boucle sur laquelle le joueur agit à part
        pass



    '''
    La boucle display nous permet la gestion des élémetns graphique et des layers d'affichage
    '''

    def display(self):
        """
        Gère l'affichage des éléments à l'écran, notez bien que l'ordre des commandes correspond à l'ordre,
        arrière plan / premier plan
        """
        self.window.fill(constants.default_color)
        self.window.blit(pygame.image.load("assets/board/export/Application_bg.png"),(0,0))
        self.board.draw_board(self.window)
        self.board.draw_pieces(self.window)

        if self.player_clicks != [] :
            self.board.draw_moves(self.window,self.Valid_moves,self.player_clicks[0])

        if self.board.checkmate or self.board.pat :
            if self.board.checkmate :
                print("Chekmate" + self.board.colour_to_play + " have lost the game")

            if self.board.pat :
                print("Pat - Partie Nulle-")

            # On mettra ici le déclencheement de l'animation de victoire et du menu rejouer.



        pygame.display.flip()



    def run(self):
        """
        Fait tourner l'application

        :return:
        """
        while self.running :
            self.events()
            self.update()
            self.display()
            self.clock.tick(constants.FPS)

if __name__ == '__main__' :
    test = Game()
    test.run()