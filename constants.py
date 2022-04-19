"""
This file contains the constant variable of the application and chess game,
its purpose is to maintain code clear and readable
"""
import pygame

pygame.font.init()


def load_pieces_images():
    Images = {}
    pieces = ['black_pawn',
              'black_king',
              'black_queen',
              'black_rock',
              'black_knight',
              'black_bishop',
              'white_pawn',
              'white_rock',
              'white_knight',
              'white_bishop',
              'white_queen',
              'white_king',
              'EmptySquare']

    for piece in pieces:
        Images[piece] = pygame.image.load("assets/board/export/pieces/03/" + piece + ".png")
        Images[piece] = pygame.transform.scale(Images[piece], (64, 64))

    return Images


name = "Chess"

FPS = 60


# Chess related stuff

def get_starting_position(p_color='white'):
    #if p_color == 'white':
        return [
            ['black_rock', 'black_knight', 'black_bishop', 'black_queen', 'black_king', 'black_bishop', 'black_knight',
             'black_rock'],
            ['black_pawn', 'black_pawn', 'black_pawn', 'black_pawn', 'black_pawn', 'black_pawn', 'black_pawn',
             'black_pawn', ],
            ["EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare",
             "EmptySquare"],
            ["EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare",
             "EmptySquare"],
            ["EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare",
             "EmptySquare"],
            ["EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare",
             "EmptySquare"],
            ['white_pawn', 'white_pawn', 'white_pawn', 'white_pawn', 'white_pawn', 'white_pawn', 'white_pawn',
             'white_pawn', ],
            ['white_rock', 'white_knight', 'white_bishop', 'white_queen', 'white_king', 'white_bishop', 'white_knight',
             'white_rock']
        ]
        """ elif p_color == 'black':
        return [
            ['white_rock', 'white_knight', 'white_bishop', 'white_queen', 'white_king', 'white_bishop', 'white_knight',
             'white_rock'],
            ['white_pawn', 'white_pawn', 'white_pawn', 'white_pawn', 'white_pawn', 'white_pawn', 'white_pawn',
             'white_pawn', ],
            ["EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare",
             "EmptySquare"],
            ["EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare",
             "EmptySquare"],
            ["EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare",
             "EmptySquare"],
            ["EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare",
             "EmptySquare"],
            ['black_pawn', 'black_pawn', 'black_pawn', 'black_pawn', 'black_pawn', 'black_pawn', 'black_pawn',
             'black_pawn', ],
            ['black_rock', 'black_knight', 'black_bishop', 'black_queen', 'black_king', 'black_bishop', 'black_knight',
             'black_rock']
        ]"""


class Game_constants :
    def __init__(self, player_colour="white"):
        self.player_colour = player_colour
        if player_colour == 'white':
            self.forward_direction = +1
            self.forward_charge = -1
            self.black_pawn_line = 1
            self.white_pawn_line = 7
            self.white_last_row = 0
            self.black_last_row = 8
        elif player_colour == 'black' :
            self.forward_direction = -1
            self.forward_charge = +1
            self.black_pawn_line = 7
            self.white_pawn_line = 1
            self.white_last_row = 8
            self.black_last_row = 0

    def change_colour(self, player_colour):
        self.player_colour = player_colour
        if player_colour == 'white':
            self.forward_direction = +1
            self.forward_charge = -1
            self.black_pawn_line = 1
            self.white_pawn_line = 7
            self.white_last_row = 0
            self.black_last_row = 8
        elif player_colour == 'black' :
            self.forward_direction = -1
            self.forward_charge = +1
            self.black_pawn_line = 7
            self.white_pawn_line = 1
            self.white_last_row = 8
            self.black_last_row = 0

def get_forward_direction(player_colour, is_charge=False):
    if player_colour == 'white':
        if is_charge:
            return +2
        return +1

    if player_colour == 'black':
        if is_charge:
            return -2
        return -1


def get_pawn_starting_line(player_colour, color):
    if player_colour == 'white':
        return 7

turn_board = {
    0 : 7,
    1 : 6,
    2 : 5,
    3 : 4,
    4 : 3,
    5 : 2,
    6 : 1,
    7 : 0,
}

quit = False


def quit_game():
    quit = True
    return quit


# Constant UI-related

Images = load_pieces_images()

image_overlay = pygame.image.load("assets/board/export/valid_move_text.png")
image_attack = pygame.image.load("assets/board/export/Attack_move.png")
image_attack = pygame.transform.scale(image_attack, (64,64))
board_offset = (64, 128)

board_position = (576, 640)

# Pygame related stuff

Arial_font = pygame.font.Font('fonts/ARIALN.TTF', 16)

default_color = pygame.Color((61, 61, 61))

error_color = pygame.Color((136, 0, 21))
