# -*- coding: utf-8 -*-

import math
import pygame
import chess_engine
import sys, time

import chess_globals_variable
import constants
import Menus

#Taille finale de l'application (704,768), taille de l'échiquier (512,512)
class Application :
    """
    Cette classe contient l'affichage de la partie d'échecs
    Je dois encore clarifier comment le faire proprement, pour l'instant il s'agit également de la gestion de l'application
    """

    def __init__(self):
        # classic pygame stuff
        self.window_size = (704,768)
        #self.screen_surface = pygame.Surface(self.window_size, flags=pygame.SRCALPHA)
        self.window = pygame.display.set_mode(self.window_size, flags=pygame.SRCALPHA)
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
        self.game = Menus.ChessGame(self.window)






    def run(self):
        """
        Fait tourner l'application

        :return:
        """

        self.game.run()


if __name__ == '__main__' :
    test = Application()
    test.run()


'''

Gestion du deltaT
previoustime = time.time()
loop :
    self.now = time.time()
    deltaT = self.now - previoustime
    previoustime = self.now
    do some shit with deltaTIme
'''