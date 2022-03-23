# -*- coding: utf-8 -*-
import pygame
import math
import constants
import stockfish_integration as ai
import re
# import images in variables
import stockfish as sf

class ChessBoard:
    """
    This class is used to interact with the rules of chess and manipulation the board.
    It does contains :
        - the board and methods to parse it
        - the moveLog that resume the state of the game
        - the stockfish ai to play with the computer

    """
    def __init__(self):
        self.image = pygame.image.load("assets/board/export/chessboard_tex.png")
        self.rect = self.image.get_rect()
        self.board = [
            ["EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare",
             "EmptySquare"],
            ["EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare",
             "EmptySquare"],
            ["EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare",
             "EmptySquare"],
            ["EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare",
             "EmptySquare"],
            ["EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare",
             "EmptySquare"],
            ["EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare",
             "EmptySquare"],
            ["EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare",
             "EmptySquare"],
            ["EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare", "EmptySquare",
             "EmptySquare"],
        ]
        self.move_LOG = []
        self.colour_to_play = "white"
        self.overlay = []
        self.white_king_location = [7, 4]
        self.black_king_location = [0, 4]
        self.checkmate = False
        self.pat = False
        self.gameover_rect = pygame.Rect(50, 50, 256, 64)
        self.check_color = pygame.Color((32, 99, 232))
        self.pat_color = pygame.Color((120, 76, 133))
        self.valid_squares = []
        # variables pour l'echec et le clouage
        self.inCheck = False
        self.clouage = []
        self.checks = []
        self.rect.move_ip(constants.board_offset)
        self.current_roques_autorisation = Roque_Autorisation(True, True, True, True)
        self.Roques_autorisation_log = [Roque_Autorisation(self.current_roques_autorisation.white_grand_roque,
                                                           self.current_roques_autorisation.white_petit_roque,
                                                           self.current_roques_autorisation.black_petit_roque,
                                                           self.current_roques_autorisation.black_grand_roque)]
        self.ongoing_promotion = False
        self.promotion_list = []
        self.stockfish = sf.Stockfish(path="stockfish_14.1_win_x64_popcnt/stockfish_14.1_win_x64_popcnt.exe")

    def next_color(self):
        if self.colour_to_play == "white":
            self.colour_to_play = "black"
            return
        if self.colour_to_play == "black":
            self.colour_to_play = "white"
            return

    def draw_checked_square(self, screen):
        for c in self.valid_squares:
            rect = pygame.Rect(c[1] * 64,
                               c[0] * 64,
                               64 + constants.board_offset[1],
                               64 + constants.board_offset[0])

            screen.blit(constants.image_overlay, rect)

    def opponent_colour(self, colour):
        if colour == "white":
            return 'black'
        if colour == "black":
            return 'white'

    def draw_board(self, screen):
        screen.blit(self.image, self.rect)

    def draw_moves(self, screen, moves, square):
        piece = self.board[square[0]][square[1]]  # piece selectionée
        for move in moves:  # pour les moves dans les moves valids
            if move.start_row == square[0] and move.start_col == square[1] and \
                    [move.start_row, move.start_col] != [move.end_row, move.end_col]:
                screen.blit(constants.image_overlay, pygame.Rect(move.end_col * 64 + constants.board_offset[0],
                                                                 move.end_row * 64 + constants.board_offset[1], 64, 64))

    def draw_pieces(self, screen):
        for row in range(8):
            for col in range(8):
                rect = pygame.Rect(row * 64 + constants.board_offset[0],
                                   col * 64 + constants.board_offset[1],
                                   64,
                                   64)
                piece = self.board[col][row]
                screen.blit(constants.Images[piece], rect)

    def get_piece_type(self, piece_square):
        '''
        Get the piece in given square
        '''
        piece = self.board[piece_square[0]][piece_square[1]]
        if piece != 'EmptySquare':
            type = piece.split('_')[1]
            return type
        else:
            return 'EmptySquare'

    def get_piece_colour(self, piece_square):
        piece = self.board[piece_square[0]][piece_square[1]]
        colour = piece[0:5]
        return colour

    def set_starting_position(self):
        self.board = constants.starting_position

    def set_promotion_menu(self, screen, promotion_square):
        piece_square = (self.move_LOG[-1].end_row,
                        self.move_LOG[-1].end_col)
        if self.colour_to_play == 'white' :
            rock_image = constants.Images['white_rock']
            bishop_image = constants.Images['white_bishop']
            knight_image = constants.Images['white_knight']
            queen_image = constants.Images['white_queen']
        if self.colour_to_play == 'black' :
            rock_image = constants.Images['black_rock']
            bishop_image = constants.Images['black_bishop']
            knight_image = constants.Images['black_knight']
            queen_image = constants.Images['black_queen']

        rock_rect = rock_image.get_rect()
        bishop_rect = bishop_image.get_rect()
        knight_rect = knight_image.get_rect()
        queen_rect = queen_image.get_rect()

        if self.colour_to_play == 'white' :
            queen_rect.move_ip(promotion_square[1] - 96, promotion_square[0]-64)
            knight_rect.move_ip(promotion_square[1] - 32, promotion_square[0] - 64)
            rock_rect.move_ip(promotion_square[1] + 32, promotion_square[0] - 64)
            bishop_rect.move_ip(promotion_square[1] + 96, promotion_square[0] - 64)
        if self.colour_to_play == 'black' :
            queen_rect.move_ip(promotion_square[1] - 96, promotion_square[0] + 64)
            knight_rect.move_ip(promotion_square[1] - 32, promotion_square[0] + 64)
            rock_rect.move_ip(promotion_square[1] + 32, promotion_square[0] + 64)
            bishop_rect.move_ip(promotion_square[1] + 96, promotion_square[0] + 64)
        print(promotion_square[0] -  96 , promotion_square[1] - 64 )
        #queen_rect.move_ip((400,30))

        """
        Position des carrés de sélection de la pièce promue :
        Reine / cavalier / Tour / Fou
        taille des carré 64x64 
        
        """
        while self.ongoing_promotion :
            mx, my = pygame.mouse.get_pos()

            screen.blit(queen_image, queen_rect)
            screen.blit(knight_image, knight_rect)
            screen.blit(rock_image, rock_rect)
            screen.blit(bishop_image, bishop_rect)

            pygame.display.flip()
            #display

            for event in pygame.event.get() :
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_ESCAPE :
                        self.ongoing_promotion = False

                if event.type == pygame.MOUSEBUTTONDOWN :
                    if event.button == 1 :
                        click = True

                    if click and queen_rect.collidepoint(mx,my) :
                        self.board[piece_square[0]][piece_square[1]] = self.colour_to_play + '_queen'
                        self.ongoing_promotion = False
                    if click and rock_rect.collidepoint(mx, my) :
                        self.board[piece_square[0]][piece_square[1]] = self.colour_to_play + '_rock'
                        self.ongoing_promotion = False
                    if click and knight_rect.collidepoint(mx, my) :
                        self.board[piece_square[0]][piece_square[1]] = self.colour_to_play + '_knight'
                        self.ongoing_promotion = False
                    if click and bishop_rect.collidepoint(mx, my) :
                        self.board[piece_square[0]][piece_square[1]] = self.colour_to_play + '_bishop'
                        self.ongoing_promotion = False





    def Make_Move(self, move):
        #Classic Move

        self.board[move.end_row][move.end_col] = move.moved_piece  # on change la pièce d'arrivée
        self.board[move.start_row][move.start_col] = "EmptySquare"  # la case de la pièce de départ devient vide
        if move.moved_piece == 'white_king':
            self.white_king_location = [move.end_row, move.end_col]
        if move.moved_piece == 'black_king':
            self.black_king_location = [move.end_row, move.end_col]

        '''
        Handle Pawn promotion
        '''
        if move.moved_piece == 'white_pawn' and move.end_row == 0 :
            move.is_promotion = True
            self.ongoing_promotion = True

        if move.moved_piece == 'black_pawn' and move.end_row == 7 :
            print("promotion")
            move.is_promotion = True
            self.ongoing_promotion = True



        """
        Handle En passant
        """
        if move.is_en_passant :
            if self.colour_to_play == 'white' :
                print('white_passing')
                print(move.end_row + 1, move.end_col)
                self.board[move.end_row + 1][move.end_col] = 'EmptySquare'
                move.captured_piece = 'black_pawn'
            if move.moved_piece == 'black_pawn' :
                self.board[move.end_row - 1][move.end_col] = 'EmptySquare'
                move.captured_piece = 'white_pawn'
            print(move.captured_piece)
        """
        Handle Roque move
        """
        if move.is_roque == True:
            tower_row = None
            tower_col = None
            tower_colour = None
            # On détermine la rangée de la tour
            if move.moved_piece == 'white_king':
                tower_row = 7
                tower_colour = 'white'
            else:
                tower_row = 0
                tower_colour = 'black'
            # On détermine la tour à bouger / le type de roque
            if move.end_col == 2 :
                print('grand roque')
                tower_col = 0
                self.board[move.start_row][move.end_col + 1] = tower_colour + '_rock'
                self.board[tower_row][tower_col] = 'EmptySquare'
            if move.end_col == 6 :
                print('petit roque')
                tower_col = 7
                self.board[move.start_row][move.end_col- 1] = tower_colour + '_rock'
                self.board[tower_row][tower_col] = 'EmptySquare'

        # Mettre à jour les droits de Roques
        self.current_roques_autorisation.Update_roque_authorisation(move)
        self.move_LOG.append(move)

    def Undo_Move(self):
        if self.move_LOG:
            last_move = self.move_LOG[-1]
            self.board[last_move.end_row][last_move.end_col] = last_move.captured_piece  # on change la pièce d'arrivée
            self.board[last_move.start_row][last_move.start_col] = last_move.moved_piece
            if last_move.moved_piece == 'white_king':
                self.white_king_location = [last_move.start_row, last_move.start_col]
            if last_move.moved_piece == 'black_king':
                self.black_king_location = [last_move.start_row, last_move.start_col]
            self.next_color()
            self.move_LOG.pop(-1)
            if last_move.is_en_passant :
                if last_move.moved_piece == 'white_pawn' :
                    self.board[last_move.end_row + 1][last_move.end_col] = last_move.captured_piece
                if last_move.moved_piece == 'black_pawn' :
                    self.board[last_move.end_row - 1][last_move.end_col] = last_move.captured_piece
                self.board[last_move.end_row][last_move.end_col] = 'EmptySquare'
            if last_move.is_roque:
                #just like Make move but reversed
                tower_row = None
                tower_col = None
                tower_colour = None
                # On détermine la rangée de la tour
                if last_move.moved_piece == 'white_king':
                    tower_row = 7
                    tower_colour = 'white'

                else:
                    tower_row = 0
                    tower_colour = 'black'
                if last_move.end_col == 2:
                    tower_col = 0
                    self.board[last_move.start_row][last_move.end_col + 1] = 'EmptySquare'
                    self.board[tower_row][tower_col] = tower_colour + '_rock'
                    if tower_colour == 'white' :
                        self.current_roques_autorisation.white_grand_roque = True
                        self.current_roques_autorisation.white_petit_roque = True

                    else :
                        self.current_roques_autorisation.black_grand_roque = True
                        self.current_roques_autorisation.black_petit_roque = True

                if last_move.end_col == 6:
                    tower_col = 7
                    self.board[last_move.start_row][last_move.end_col - 1] = 'EmptySquare'
                    self.board[tower_row][tower_col] = tower_colour + '_rock'
                    if tower_colour == 'white' :
                        self.current_roques_autorisation.white_petit_roque = True
                        self.current_roques_autorisation.white_grand_roque = True
                    else :
                        self.current_roques_autorisation.black_petit_roque = True
                        self.current_roques_autorisation.black_grand_roque = True

        else:
            print("no moves to undo, trait aux blancs!")

    def get_all_possibles_moves(self, player_colour):
        moves = []
        for rows in range(len(self.board)):  # Pour tout ligne
            for c in range(len(self.board[rows])):  # pour toute col in ligne
                # voir la couleur de la pièce
                piece_square = [rows, c]
                colour = self.get_piece_colour(piece_square)
                type = self.get_piece_type(piece_square)
                if colour == player_colour:
                    if type == "pawn":
                        self.get_Pawn_moves(rows, c, moves, colour)

                    elif type == 'knight':
                        self.get_Knight_moves(rows, c, moves, colour)

                    elif type == 'bishop':
                        self.get_Bishop_moves(rows, c, moves, colour)

                    elif type == 'rock':
                        self.get_Rock_moves(rows, c, moves, colour)

                    elif type == 'queen':
                        self.get_Queen_moves(rows, c, moves, colour)

                    elif type == 'king':
                        self.get_King_moves(rows, c, moves, colour)
                        self.get_Roque_Moves(rows, c, moves, colour)
                else:
                    pass

        return moves

    def get_all_moves_without_Roque(self, player_colour):
        '''
        Génération de tous les coups dans les roques pour éviter les boucles infinies

        Cette fonction dpoit sûrement disparaître

        :param player_colour:
        :return:
        '''
        moves = []
        for rows in range(len(self.board)):  # Pour tout ligne
            for c in range(len(self.board[rows])):  # pour toute col in ligne
                # voir la couleur de la pièce
                piece_square = [rows, c]
                colour = self.get_piece_colour(piece_square)
                type = self.get_piece_type(piece_square)
                if colour == player_colour:
                    if type == "pawn":
                        self.get_Pawn_moves(rows, c, moves, colour)
                    elif type == 'knight':
                        self.get_Knight_moves(rows, c, moves, colour)
                    elif type == 'bishop':
                        self.get_Bishop_moves(rows, c, moves, colour)
                    elif type == 'rock':
                        self.get_Rock_moves(rows, c, moves, colour)
                    elif type == 'queen':
                        self.get_Queen_moves(rows, c, moves, colour)
                    elif type == 'king':
                        self.get_King_moves(rows, c, moves, colour)
                    else:
                        pass

        return moves

    def square_under_attack(self, r, c, color):
        '''
        Cette méthode permet de vérifier si la case position (r,c) est sous l'attaque de la couleur inverse de colour
        :param r:
        :param c:
        :param color:
        :return:
        '''
        op_color = self.opponent_colour(color)
        opponent_moves = self.get_all_moves_without_Roque(op_color)
        for move in opponent_moves:
            if move.end_row == r and move.end_col == c:
                return True
            else:
                pass
        return False

    def get_Valid_moves(self, colour):
        '''
        Valid move est la méthode de génération des moves définitifs, elle sert de relation entre la méthode naive de génération
        des coups simples et les règles plus complexes (échecs, clouage) qui impliquent le Roi

        Elle prend en input la couleur qui doit jouer et fait appels aux fonctions :
        self.get_all_possible_moves(colour)
        self.check_for_pins_and_check(colour)

        :param colour:
        :return:
        '''
        legal_moves = []
        if colour == 'white':
            king_loc = self.white_king_location
        else:
            king_loc = self.black_king_location
        self.inCheck, self.clouage, self.checks = self.check_for_pins_and_checks(colour)
        if self.inCheck:  # nous sommes en echec/ nous allons générer les réponses à l'échec
            '''
            Pour chaque echec (case + direction), générons les réopnses possible
            '''
            if len(self.checks) == 1:
                legal_moves = self.get_all_possibles_moves(colour)
                check = self.checks[0]
                check_row = check[0]
                check_col = check[1]
                checking_piece = self.board[check_row][check_col]
                self.valid_squares = []  # cases sur lesquelles une pièce peut bouger pour empêcher l'échec
                if self.get_piece_type([check_row,
                                        check_col]) == 'knight':  # on ne peut pas bloquer le cavalier, il faut bouger le roi ou manger le cavalier
                    self.valid_squares.append((check_row, check_col))
                    # la seule pièce que l'on peut manger est le cavalier pour empêcher l'échec
                else:
                    for i in range(1, 8):
                        valid_square = (king_loc[0] + i * check[2], king_loc[1] + i * check[3])
                        self.valid_squares.append(valid_square)
                        if valid_square[0] == check_row and valid_square[1] == check_col:
                            break
                # il faut se débarasser des moves qui n'enlèvent pas l'échec

                for i in range(len(legal_moves) - 1, -1,
                               -1):  # on boucle à l'envers pour retirer les éléments d'une liste
                    if self.get_piece_type([legal_moves[i].start_row, legal_moves[i].start_col]) != 'king':
                        # si le move n'est pas un move du roi alors il doit bloquer ou manger la pièce, finir sur une valid square
                        if not (legal_moves[i].end_row, legal_moves[i].end_col) in self.valid_squares:
                            legal_moves.remove(legal_moves[i])

            else:  # double ou triple echecs on ne peut bloquer les pièce il faut boueger le roi
                legal_moves = self.get_King_moves(king_loc[0], king_loc[1], legal_moves, colour)
            pass
        else:  # nous ne sommes pas en echecs nous pouvons analyser les moves possibles
            legal_moves = self.get_all_possibles_moves(colour)  # on génère une fois tous les moves possibles

        if len(legal_moves) == 0:
            if self.inCheck:
                self.checkmate = True
            else:
                self.pat = True


        return legal_moves

    # cet algorithme plus élégant ne recalcule plus tous le coups de l'adversaire pour voir si le roi est en echecs en traquant sa position
    # mais il part de la position du roi pour savoir si une pièce ennemi peut l'attaquer

    def check_for_pins_and_checks(self, colour):
        clouage = []  # contient les cases clouées par l'adversaire
        echecs = []  # contient les case avec les pièce attaquant le roi
        incheck = False  # par défaut
        op_colour = self.opponent_colour(colour)
        if colour == 'white':
            king_loc = self.white_king_location
        if colour == 'black':
            king_loc = self.black_king_location

        # algorithme inverse des coups des pièce,on gère les cavaliers à part
        directions = ((0, -1), (0, +1), (+1, 0), (-1, 0),
                      (-1, -1), (-1, +1), (+1, -1), (+1, +1))
        for j in range(len(directions)):
            possible_pin = ()
            d = directions[j]
            for i in range(1,
                           8):  # pour chaque case on ajoute l'offset multiplié par l'itération => case finale du move
                check_row = king_loc[0] + i * d[0]
                check_col = king_loc[1] + i * d[1]
                #inside Board
                if 0 <= check_col <= 7 and 0 <= check_row <= 7:
                    #check_piece
                    check_piece = self.board[check_row][check_col]
                    # if
                    if self.get_piece_colour([check_row, check_col]) == colour and \
                            self.get_piece_type([check_row, check_col]) != 'king':  # pièce alliée clouage possible
                        if possible_pin == ():
                            possible_pin = (check_row, check_col, d[0], d[1])
                        else:  # je suis protégé par deux pièces il n'y a pas de clouage
                            break
                    elif self.get_piece_colour([check_row, check_col]) == op_colour:
                        # il y une pièece adverse vérifier l'échec
                        '''
                        condition complexe ici : nous sommes en echec si :
                        1) nous vérifions une colonne et la pièce est une tour
                        2) nous vérifions en diagonale et la pièce est un fou
                        3) nous vérifions les diagonales avant et la piièce est un pion 
                        4) la pièce est une dame (peut importe la direction)
                        5) il y a un roi deux case plus loin (pour empêcher le deplacement de notre roi sur une pièce controlé par un roi adverse)
                        '''
                        piece_type = self.get_piece_type([check_row, check_col])
                        if (0 <= j <= 3 and piece_type == 'rock') or \
                            (4 <= j <= 7 and piece_type == 'bishop') or \
                            (piece_type == 'queen') or \
                            (i == 1 and piece_type == 'king') or \
                            (i == 1 and ((colour == 'white' and 4 <= j <= 5) or (colour == 'black' and 6 <= j <= 7))):
                            if possible_pin == ():  # il n'y a pas de pièce qui peut défendre le roi
                                incheck = True
                                echecs.append((check_row, check_col, d[0], d[1]))
                                break
                            else:  # la pièce devient clouée
                                clouage.append(possible_pin)
                                break
                        else:  # la pièce ne peut pas attaquer le roi ( par exemple la pièce est un cavalier adverse)
                            break
                    else : #square is empty
                        pass
                else:  # nous sommes sorti de l'échiquier
                    break
        # nous pouvons maintenant vérifier si les case de type cavaliers menace le roi
        knights_moves = ((-1, -2), (-1, +2), (+2, -1), (+2, +1),
                         (-2, -1), (-2, +1), (+1, -2), (+1, +2))
        for m in knights_moves:
            check_row = king_loc[0] + m[0]
            check_col = king_loc[1] + m[1]
            if 0 < check_col < 8 and 0 < check_row < 8:  # on vérifie que l'on est sur le board
                if self.get_piece_type([check_row, check_col]) == 'knight' and \
                        self.get_piece_colour([check_row, check_col]) == op_colour:
                    incheck = True
                    echecs.append((check_row, check_col, m[0], m[1]))
                    break
        return incheck, clouage, echecs




    def get_Roque_Moves(self, r, c, moves, colour):
        '''
        Un Roque est un Move constitué de deux moves
        1) le roi se déplace de deux cases vers la Tour si aucune des case n'est en échec
        2) La tour se place derrière le Roi
        :return:
        '''
        if self.inCheck:
            return
        if colour == 'white':
            king_loc = self.white_king_location
            if self.current_roques_autorisation.white_grand_roque:
                if self.board[r][c - 1] == 'EmptySquare' and self.board[r][c - 2] == 'EmptySquare':
                    if not (self.square_under_attack(r, c - 2, self.colour_to_play) or
                            self.square_under_attack(r, c -1 , self.colour_to_play)):
                        grand_roque = Move([r, c], [r, c - 2], self.board, is_roque= True)
                        moves.append(grand_roque)

            if self.current_roques_autorisation.white_petit_roque:
                if self.board[r][c + 1] == 'EmptySquare' and self.board[r][c + 2] == 'EmptySquare':

                    if  (not self.square_under_attack(r,c + 2, self.colour_to_play) and
                           not self.square_under_attack(r,c + 1,self.colour_to_play)):

                        petit_roque = Move([r, c], [r, c + 2], self.board, is_roque= True)
                        moves.append(petit_roque)

        elif colour == 'black':
            king_loc = self.black_king_location
            if self.current_roques_autorisation.black_grand_roque:
                if self.board[r][c - 1] == 'EmptySquare' and self.board[r][c - 2] == 'EmptySquare':
                    if  (not self.square_under_attack(r, c - 2, self.colour_to_play) or
                            not self.square_under_attack(r, c - 1, self.colour_to_play)) :
                        grand_roque = Move([r, c], [r, c - 2], self.board, is_roque=True)
                        moves.append(grand_roque)

            if self.current_roques_autorisation.black_petit_roque:
                if not (self.square_under_attack(r, c + 2, self.colour_to_play) or
                        self.square_under_attack(r, c + 1, self.colour_to_play)):

                    petit_roque = Move([r, c], [r, c + 2], self.board, is_roque=True)
                    moves.append(petit_roque)
        else:
            return

        # Grand Roque blanc :



    '''
    Pieces moves by piece type, j'ai rajouté pour faire fonctionner l'algorithme complexe abordé par le tuto
    la variable piece_cloue = True/False
    '''

    def get_Pawn_moves(self, r, c, moves, colour):
        # obtenir les coups possible du pion à la position r, c et les ajouter à moves
        piece_clouee = False
        pin_direction = ()
        for i in range(len(self.clouage) - 1, -1, -1):
            if self.clouage[i][0] == r and self.clouage[i][1] == c:
                piece_clouee = True
                pin_direction = (self.clouage[i][2], self.clouage[i][3])
                self.clouage.remove(self.clouage[i])
                break
        '''
        Gestion du en passant
        Le move en passant peut se faire sous deux conditions :
        le pion se trouve sur la rangée 3 (blancs) ou 4 (noir)
        le précédent coup était une charge d'un pion à côté de la pièce 
        '''
        if colour == 'white':
            if 0 <= r <= 7 and 0 <= c <= 7:
                if len(self.move_LOG) != 0:
                    if self.move_LOG[-1].is_pawn_charge :
                        if (self.move_LOG[-1].end_col == c + 1 or self.move_LOG[-1].end_col == c - 1) and \
                        r == 3 :
                            moves.append(
                                Move([r, c], [self.move_LOG[-1].end_row - 1, self.move_LOG[-1].end_col], self.board, False, False,
                                     True))
                if self.board[r - 1][c] == 'EmptySquare' :
                    if not piece_clouee or pin_direction == (0, -1):
                        moves.append(Move([r, c], [r - 1, c], self.board))  # on avance d'une case s'il n'y a pas de pièce
                if r == 6 and self.board[r - 2][c] == 'EmptySquare' and self.board[r - 1][c] == 'EmptySquare':
                    if not piece_clouee or pin_direction == (0, -1):
                        moves.append(Move([r, c], [r - 2, c], self.board,False, True))
                if c + 1 <= 7:
                    if self.get_piece_colour([r - 1, c + 1]) == 'black':
                        if not piece_clouee or pin_direction == (-1, 1):
                            moves.append(Move([r, c], [r - 1, c + 1], self.board))
                if c - 1 >= 0:
                    if self.get_piece_colour([r - 1, c - 1]) == 'black':
                        if not piece_clouee or pin_direction == (-1, -1):
                            moves.append(Move([r, c], [r - 1, c - 1], self.board))
        if colour == 'black':
            if 0 <= r <= 7 and 0 <= c <= 7 :
                if len(self.move_LOG) != 0:
                    if self.move_LOG[-1].is_pawn_charge :
                        if (self.move_LOG[-1].end_col == c + 1 or self.move_LOG[-1].end_col == c - 1) and \
                        r == 4:
                            moves.append(
                                Move([r, c],
                                     [self.move_LOG[-1].end_row + 1, self.move_LOG[-1].end_col],
                                     self.board,
                                     False,
                                     False,
                                     True ))
                    if r != 7 :
                        if self.board[r + 1][c] == 'EmptySquare' :
                            if not piece_clouee or pin_direction == (1, 0):
                                moves.append(Move([r, c], [r + 1, c], self.board))
                        if r == 1 and (self.board[r + 2][c] == 'EmptySquare' and self.board[r+1][c] == 'EmptySquare'):
                            if not piece_clouee or pin_direction == (1, 0):
                                charge = Move([r, c], [r + 2, c], self.board, False,True)
                                moves.append(Move([r, c], [r + 2, c], self.board, False,True))
                        if c + 1 <= 7:
                            if self.get_piece_colour([r + 1, c + 1]) == 'white':
                                if not piece_clouee or pin_direction == (1, 1):
                                    moves.append(Move([r, c], [r + 1, c + 1], self.board))
                        if c - 1 >= 0:
                            if self.get_piece_colour([r + 1, c - 1]) == 'white':
                                if not piece_clouee or pin_direction == (1, -1):
                                    moves.append(Move([r, c], [r + 1, c - 1], self.board))

    def get_Knight_moves(self, r, c, moves, colour):
        piece_clouee = False
        pin_direction = ()
        for i in range(len(self.clouage) - 1, -1, -1):
            if self.clouage[i][0] == r and self.clouage[i][1] == c:
                piece_clouee = True
                pin_direction = (self.clouage[i][2], self.clouage[i][3])
                self.clouage.remove(self.clouage[i])
                break

        directions = ((-1, -2), (-1, +2), (+2, -1), (+2, +1),
                      (-2, -1), (-2, +1), (+1, -2), (+1, +2))

        for d in directions:
            if not piece_clouee:
                end_row = r + d[0]
                end_col = c + d[1]
                if 0 <= end_row < 8 and 0 <= end_col < 8:  # on est sur le board
                    if self.board[end_row][end_col] == 'EmptySquare':
                        moves.append(Move([r, c], [end_row, end_col], self.board))
                    elif self.get_piece_colour([end_row, end_col]) != colour:
                        moves.append(Move([r, c], [end_row, end_col], self.board))
                    else:
                        pass

    def get_Bishop_moves(self, r, c, moves, colour):

        piece_clouee = False
        pin_direction = ()

        for i in range(len(self.clouage) - 1, -1, -1):
            if self.clouage[i][0] == r and self.clouage[i][1] == c:
                piece_clouee = True
                pin_direction = (self.clouage[i][2], self.clouage[i][3])
                self.clouage.remove(self.clouage[i])
                break

        # On cherche les coups possibles pour le bishop à la position self.board[r][c] si le move est autorisé, on ajoute à moves
        directions = ((-1, -1), (-1, +1), (+1, -1), (+1, +1))
        for d in directions:
            if not piece_clouee or pin_direction == d:
                for i in range(1,
                               8):  # pour chaque case on ajoute l'offset multiplié par l'itération => case finale du move
                    end_row = r + i * d[0]
                    end_col = c + i * d[1]
                    if 8 > end_col >= 0 and 8 > end_row >= 0:  # On est sur l'echiquier
                        end_piece = self.board[end_row][end_col]
                        if end_piece == 'EmptySquare':  # case vide
                            moves.append(Move([r, c], [end_row, end_col], self.board))
                        elif self.get_piece_colour([end_row, end_col]) != colour:  # pièce adverse
                            moves.append(Move([r, c], [end_row, end_col], self.board))
                            break  # on ne peut pas aller plus loin dans cette direction, break casse la loop direction
                        else:  # le dernier cas est une pièce alliée
                            break
                    else:  # on sort du board
                        break

    def get_Rock_moves(self, r, c, moves, colour):
        piece_clouee = False
        pin_direction = ()
        for i in range(len(self.clouage) - 1, -1, -1):
            if self.clouage[i][0] == r and self.clouage[i][1] == c:
                piece_clouee = True
                pin_direction = (self.clouage[i][2], self.clouage[i][3])
                self.clouage.remove(self.clouage[i])
                break
        # même fonctionnement que pour le fou mais on change les directions
        directions = ((0, -1), (0, +1), (+1, 0), (-1, 0))
        for d in directions:
            if not piece_clouee or pin_direction == d:
                for i in range(1,
                               8):  # pour chaque case on ajoute l'offset multiplié par l'itération => case finale du move
                    end_row = r + i * d[0]
                    end_col = c + i * d[1]
                    if 8 > end_col >= 0 and 8 > end_row >= 0:  # On est sur l'echiquier
                        end_piece = self.board[end_row][end_col]

                        if end_piece == 'EmptySquare':  # case vide
                            moves.append(Move([r, c], [end_row, end_col], self.board))

                        elif self.get_piece_colour([end_row, end_col]) != colour:  # pièce adverse
                            moves.append(Move([r, c], [end_row, end_col], self.board))
                            break  # on ne peut pas aller plus loin dans cette direction, break casse la loop direction

                        elif self.get_piece_colour([end_row, end_col]) != colour:  # le dernier cas est une pièce alliée
                            break
                        else:
                            break

                    else:  # on sort du board
                        break

    def get_Queen_moves(self, r, c, moves, colour):
        piece_clouee = False
        pin_direction = ()
        for i in range(len(self.clouage) - 1, -1, -1):
            if self.clouage[i][0] == r and self.clouage[i][1] == c:
                piece_clouee = True
                pin_direction = (self.clouage[i][2], self.clouage[i][3])
                self.clouage.remove(self.clouage[i])
                break
        # même fonctionnement que pour la tour mais on fusionne les directions du fou et de la tour
        directions = ((0, -1), (0, +1), (+1, 0), (-1, 0),
                      (-1, -1), (-1, +1), (+1, -1), (+1, +1))
        for d in directions:
            if not piece_clouee or pin_direction == d:
                for i in range(1,
                               8):  # pour chaque case on ajoute l'offset multiplié par l'itération => case finale du move
                    end_row = r + i * d[0]
                    end_col = c + i * d[1]
                    if 8 > end_col >= 0 and 8 > end_row >= 0:  # On est sur l'echiquier
                        end_piece = self.board[end_row][end_col]

                        if end_piece == 'EmptySquare':  # case vide
                            moves.append(Move([r, c], [end_row, end_col], self.board))

                        elif self.get_piece_colour([end_row, end_col]) != colour:  # pièce adverse
                            moves.append(Move([r, c], [end_row, end_col], self.board))

                            break  # on ne peut pas aller plus loin dans cette direction, break casse la loop direction
                        else:  # le dernier cas est une pièce alliée
                            break
                    else:  # on sort du board
                        break

    def get_King_moves(self, r, c, moves, colour):
        """
        On retourne les moves du Roi, c'est ici que l'on vérifie que le Roi ne se met pas en échecs
        en mangeant une pièce. cela se fait en utilisant la méthode self.chec_for_pins_and_checks(colour)
        du board
        :param r:
        :param c:
        :param moves:
        :param colour:
        :return:
        """

        directions = ((0, -1), (0, +1), (+1, 0), (-1, 0),
                      (-1, -1), (-1, +1), (+1, -1), (+1, +1))
        for d in directions:
            end_col = c + d[1]
            end_row = r + d[0]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                if self.get_piece_colour([end_row, end_col]) != colour :
                    """
                    Update king location to check for checks
                    """
                    if colour == 'white':
                        self.white_king_location = [end_row, end_col]
                    if colour == 'black':
                        self.black_king_location = [end_row, end_col]

                    in_check, clouage, echecs = self.check_for_pins_and_checks(colour)
                    if in_check :
                        print("possible check")
                    if not in_check:
                        moves.append(Move([r, c], [end_row, end_col], self.board))
                    """
                    Reset king location to previous (r,c)
                    """
                    if colour == 'white':
                        self.white_king_location = [r, c]
                    if colour == 'black':
                        self.black_king_location = [r, c]
                else:
                    pass
            else:
                pass

        # check if king is attacked
        # check if castling cases are attacked
        # check if tower and king have moved
        # vérifier dans le log si aucun move n'est parti de la case du roi ou de la tour
        # check that castling cases are EmptySquare
        # le roque contient deux moves"""

    def capture_LOG(self):
        capture_LOG = []
        for move in self.move_LOG :
            capture_LOG.append(move.captured_piece)
        return capture_LOG

    def get_FEN(self):
        FEN = ""
        for row in range(8) :
            row_notation = ""
            empty_spaces = 0
            for col in range(8) :
                if self.board[row][col] == 'EmptySquare' :
                    empty_spaces += 1
                    if col == 7 :
                        row_notation += str(empty_spaces)
                else :
                    if empty_spaces != 0 :
                        row_notation += str(empty_spaces)
                        empty_spaces = 0
                    if self.board[row][col] == 'white_rock' :
                        row_notation += 'R'
                    if self.board[row][col] == 'white_knight':
                        row_notation += 'N'
                    if self.board[row][col] == 'white_bishop':
                        row_notation += 'B'
                    if self.board[row][col] == 'white_king':
                        row_notation += 'K'
                    if self.board[row][col] == 'white_queen':
                        row_notation += 'Q'
                    if self.board[row][col] == 'white_pawn':
                        row_notation += 'P'
                    if self.board[row][col] == 'black_rock' :
                        row_notation += 'r'
                    if self.board[row][col] == 'black_knight':
                        row_notation += 'n'
                    if self.board[row][col] == 'black_bishop':
                        row_notation += 'b'
                    if self.board[row][col] == 'black_king':
                        row_notation += 'k'
                    if self.board[row][col] == 'black_queen':
                        row_notation += 'q'
                    if self.board[row][col] == 'black_pawn':
                        row_notation += 'p'

            if row != 7 :
                row_notation += "/"
            FEN += row_notation

        if self.colour_to_play == 'white' :
            FEN += " w"
        else :
            FEN += " b"
        roques = " "
        if self.current_roques_autorisation.white_petit_roque :
            roques += 'K'
        if self.current_roques_autorisation.white_grand_roque :
            roques += 'Q'
        if self.current_roques_autorisation.black_petit_roque :
            roques += 'k'
        if self.current_roques_autorisation.black_grand_roque :
            roques += 'q'
        if roques == ' ':
            roques == '-'
        FEN += roques
        if  self.move_LOG != [] :
            last_move = self.move_LOG[-1]
            if last_move.is_pawn_charge :
                if self.colour_to_play == 'white' :
                    case = last_move.getLetterRow(last_move.end_row - 1, last_move.end_col)
                if self.colour_to_play == 'black' :
                    case = last_move.getLetterRow(last_move.end_row + 1, last_move.end_col)
                FEN += ' '+ case
            else :
                FEN +=' -'
        else :
            FEN += ' -'
        captures = self.capture_LOG()
        move_from_last_capture = 0
        for i in range(len(captures) -1, -1, -1) :
            if captures[i] == 'EmptySquare':
                move_from_last_capture += 1
            else :
                break
        FEN += ' ' + str(move_from_last_capture)

        FEN += ' ' + str(math.trunc(len(self.move_LOG) / 2))

        return FEN



    def algebric_to_Move(self,algebric_notation):
        letter_to_col = {"h": 7, "g": 6, "f": 5, "e": 4, "d": 3,
                         "c": 2, "b": 1, "a": 0}
        row_to_rank = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3,
                       "6": 2, "7": 1, "8": 0}
        print(algebric_notation)
        if len(algebric_notation) == 4:
            regex_pattern = r"([a-h])([1-8])([a-h])([1-8])"
            results = re.findall(regex_pattern, algebric_notation)[0]
            start_col = letter_to_col[results[0]]
            start_row = row_to_rank[results[1]]
            end_col = letter_to_col[results[2]]
            end_row = row_to_rank[results[3]]
            colour = self.get_piece_colour([start_row, start_col])
            type = self.get_piece_type([start_row, start_col])
            roque = False
            if type == 'king' :
                if end_col -start_col == 2 :
                    # petit roque
                    roque = True
                if end_col - start_col == -2 :
                    # grand roque
                    roque = True
            computer_move = Move([start_row, start_col], [end_row, end_col], self.board, is_roque=roque, is_cpu_move=True )
            return computer_move
        if len(algebric_notation) == 5 :
            print(algebric_notation)

        # fprint(((start_row,start_col),(end_row,end_col)))


    def do_best_move(self, fen_notation):
        self.stockfish.set_fen_position(fen_notation)
        notation = self.stockfish.get_best_move()
        move = self.algebric_to_Move(notation)
        return move

class Move:
    '''
    This class contains all elements defining a chess move.
    It must be modified with further implementation (i.e. computer moves)
    '''
    ranks_to_row = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3,
                    "6": 2, "7": 1, "8": 0}
    row_to_ranks = {v: k for k, v in ranks_to_row.items()}
    col_to_letter = {"h": 7, "g": 6, "f": 5, "e": 4, "d": 3,
                     "c": 2, "b": 1, "a": 0}
    letter_to_col = {v: k for k, v in col_to_letter.items()}

    def __init__(self, start_sq, end_sq, board, is_roque = False, is_pawn_charge = False, is_en_passant = False, is_promotion = False, is_cpu_move = False):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.moved_piece = board[self.start_row][self.start_col]
        self.captured_piece = board[self.end_row][self.end_col]
        self.moveID = self.start_row * 1000 + self.start_col * 100 + self.end_col * 10 + self.end_row
        self.is_roque = is_roque
        self.is_pawn_charge = is_pawn_charge
        self.is_en_passant = is_en_passant
        self.is_promotion = is_promotion
        self.is_cpu_move = is_cpu_move
        self.cpu_promotion = None

    '''
    Nous devons comparer les les Moves générés par les clics et les moves autorisés générés par le jeu. 
    Comme nous devons comparer deux moves, nous devons comparer un élément qui serra commun aux mêmes moves.
    Il s'agit du move ID 
    
    __eq__(self, other) est une fonction automatique, elle est appellée à chaque utilisation de == (eq) et override
    lorsque les deux moves sont comparés, si ils possèdent les même ID l'opérateur == renvoie TRUE 
    '''
    # se renseigner sur la fonciton __eq__(self, other)
    def __eq__(self, other):
        if isinstance(other, Move):
            if self.moveID == other.moveID :
                self.is_pawn_charge = other.is_pawn_charge
                self.is_en_passant = other.is_en_passant
                self.is_promotion = other.is_promotion
                return True
        return False


    def get_notation(self):
        return self.getLetterRow(self.start_row, self.start_col) + self.getLetterRow(self.end_row, self.end_col)

    def getLetterRow(self, r, c):
        return self.letter_to_col[c] + self.row_to_ranks[r]

    def get_cases(self):
        cases = [(self.start_row, self.start_col), (self.end_row, self.end_col)]
        return cases


class Roque_Autorisation:
    """
    Cette classe permet de traquer les autorisations de roques pour les deux couleurs et les deux types
    de roques (grand roque, petit roque) :
    -le roi ne peut plus roquer des deux côtés si il a bougé
    -le roi ne peut plus roquer d'un côté si la tour de ce côté a roqué

    """

    def __init__(self, white_grand_roque, white_petit_roque, black_petit_roque, black_grand_roque):
        self.white_grand_roque = white_petit_roque
        self.white_petit_roque = white_petit_roque
        self.black_grand_roque = black_grand_roque
        self.black_petit_roque = black_petit_roque

    def Update_roque_authorisation(self, move):
        """
        Cette méthode met à jour les autorisations de roque en vérifiant si la pièce bougée  par le correspond au roi
        ou aux tours

        :param move:
        :return:
        """
        if move.moved_piece == 'black_king':
            self.black_grand_roque = False
            self.black_petit_roque = False
        elif move.moved_piece == 'white_king':
            self.white_grand_roque = False
            self.white_petit_roque = False

        elif move.moved_piece == 'white_rock':
            if (move.start_row, move.start_col) == (7, 0):
                self.white_grand_roque = False
            if (move.start_row, move.start_col) == (7, 7):
                self.white_petit_roque = False

        elif move.moved_piece == 'black_rock':
            if (move.start_row, move.start_col) == (0, 0):
                self.black_grand_roque = False
            if (move.start_row, move.start_col) == (0, 7):
                self.black_petit_roque = False


