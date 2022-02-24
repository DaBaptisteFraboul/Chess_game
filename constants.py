"""
This file contains the constant variable of the application and chess game,
its purpose is to maintain code clear and readable
"""
import pygame
import pygame_loading
pygame.font.init()


name = "Chess"

FPS = 60
# Chess related stuff

starting_position = [
    ['black_rock', 'black_knight','black_bishop', 'black_queen','black_king', 'black_bishop','black_knight', 'black_rock'],
    ['black_pawn','black_pawn','black_pawn','black_pawn','black_pawn','black_pawn','black_pawn','black_pawn',],
    ["EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare" ],
    ["EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare" ],
    ["EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare" ],
    ["EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare" ],
    ['white_pawn', 'white_pawn', 'white_pawn', 'white_pawn', 'white_pawn', 'white_pawn', 'white_pawn', 'white_pawn', ],
    ['white_rock', 'white_knight', 'white_bishop', 'white_queen', 'white_king', 'white_bishop', 'white_knight',
     'white_rock']
]

# Constant UI-related

Images = pygame_loading.load_pieces_images()

image_overlay = pygame.image.load("assets/board/export/valid_move_text.png")

board_offset = (64, 128)

board_position= (576, 640 )

#Pygame related stuff

Arial_font = pygame.font.Font('fonts/ARIALN.TTF',16)

default_color = pygame.Color((61,61,61))

error_color = pygame.Color((136,0,21))