import pygame


def load_pieces_images() :
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

    for piece in pieces :
        Images[piece] = pygame.image.load("assets/board/export/pieces/02/" + piece + ".png")
        Images[piece] = pygame.transform.scale(Images[piece], (64,64))

    return Images


