import pygame
import math
# import images in variables

# TODO: Attention à ton utilisation des modules python.
#  Tu déclares beaucoup de chose au chargement des modules.
#  Ce module ne devrait contenir que les  classes et fonctions relatives au
#  fonctionnement (abstrait) du jeu d'échec. Hors tu charges aussi les images
#  pour pygame. Mets tout ce qui est relatif à pygame dans un autre module.


# TODO: Attention à ta nomenclature. On retrouve des méthodes ou attributs
#  nommées Get_Function, d'autres get_function, d'autres get_FUNCTIONS.
#  En python, La convention c'est PEP8: https://www.python.org/dev/peps/pep-0008/


# TODO: Ces trois lignes s'exécute lors de l'import. C'est pas top.
Images = {}
image_overlay = pygame.image.load("assets/board/export/valid_move_text.png")
board_offset = (64, 128)


def load_pieces_images() :
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
              'Empty']
    for piece in pieces :
        Images[piece] = pygame.image.load("assets/board/export/pieces/02/" + piece + ".png")
        Images[piece] = pygame.transform.scale(Images[piece], (64,64))
load_pieces_images()


# TODO: Ça, ça devrait être dans un module pour les constantes.
starting_position = [
    ['black_rock', 'black_knight','black_bishop', 'black_queen','black_king', 'black_bishop','black_knight', 'black_rock'],
    ['black_pawn','black_pawn','black_pawn','black_pawn','black_pawn','black_pawn','black_pawn','black_pawn',],
    ["Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty" ],
    ["Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty" ],
    ["Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty" ],
    ["Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty" ],
    ['white_pawn', 'white_pawn', 'white_pawn', 'white_pawn', 'white_pawn', 'white_pawn', 'white_pawn', 'white_pawn', ],
    ['white_rock', 'white_knight', 'white_bishop', 'white_queen', 'white_king', 'white_bishop', 'white_knight',
     'white_rock']
]

class ChessBoard() :
    def __init__(self):
        self.image = pygame.image.load("assets/board/export/chessboard_tex.png")
        self.rect = self.image.get_rect()
        # TODO: self.board = [["Empty"] * 8] * 8
        #  ça ferait la même chose
        self.board = [
    ["Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty"],
    ["Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty"],
    ["Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty"],
    ["Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty"],
    ["Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty"],
    ["Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty"],
    ["Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty"],
    ["Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty"],
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
        self.rect.move_ip(board_offset)
        self.current_roques_autorisation = Roque_Autorisation(True, True, True, True)
        self.Roques_autorisation_log = [Roque_Autorisation(self.current_roques_autorisation.white_grand_roque,
                                                           self.current_roques_autorisation.white_petit_roque,
                                                           self.current_roques_autorisation.black_petit_roque,
                                                           self.current_roques_autorisation.black_grand_roque)]
    '''
    def draw_endgame(self,screen):
    if self.checkmate:
        screen.blit(self.gameover_rect, self.check_color)
    if self.pat:
        screen.blit(self.gameover_rect, self.pat_color)

    '''

    def next_color(self):
        if self.colour_to_play == "white" :
            self.colour_to_play = "black"
            return
        if self.colour_to_play == "black" :
            self.colour_to_play = "white"
            return

    def draw_checked_square(self, screen):
        for c in self.valid_squares :
            rect = pygame.Rect(c[1]*64,c[0]*64, 64 + board_offset[1], 64+board_offset[0])
            screen.blit( image_overlay, rect)

    def opponent_colour(self,colour):
        if colour == "white" :
            return 'black'
        if colour == "black" :
            return 'white'

    def draw(self,screen):  # TODO: draw what? le board j'imagine? Appelle cette méthode draw_board
        screen.blit(self.image, self.rect)

    def draw_moves(self, screen, moves, square):  # TODO: Là c'est bon. :)
        piece = self.board[square[0]][square[1]] #piece selectionée
        for move in moves : #pour les moves dans les moves valids
            if move.start_row == square[0] and move.start_col == square[1] and \
                    [move.start_row, move.start_col] != [move.end_row, move.end_col] :
                screen.blit(image_overlay, pygame.Rect(move.end_col*64 + board_offset[0],move.end_row*64 + board_offset[1],64,64))


    def draw_pieces(self, screen):  # TODO: Là aussi. :)
        for row in range(8) :
            for col in range(8) :
                screen_pos = (col , row)
                piece = self.board[col][row]
                screen.blit(Images[piece], pygame.Rect(row*64 + board_offset[0],col*64+board_offset[1], 64,64))

    def get_piece_type(self, piece_square):
        piece = self.board[piece_square[0]][piece_square[1]]
        if piece != 'Empty' :
            type = piece.split('_')[1]  # TODO: attention, type c'est un mot réservé python. Il ne faut pas le redéfinir sous peine de surprise.
            return type
        else :
            return 'Empty'

    def get_piece_colour(self, piece_square):
        piece = self.board[piece_square[0]][piece_square[1]]
        colour = piece[0:5]
        return colour

    def set_starting_position(self) :
        self.board = starting_position

    def Make_Move(self, move):

        self.board[move.end_row][move.end_col] = move.moved_piece # on change la pièce d'arrivée
        self.board[move.start_row][move.start_col] = "Empty" # la case de la pièce de départ devient vide
        if move.moved_piece == 'white_king' :
            self.white_king_location = [move.end_row, move.end_col]
        if move.moved_piece == 'black_king' :
            self.black_king_location = [move.end_row, move.end_col]

        if move.is_roque:
            pass
        # Mettre à jour les droits de Roques
        self.current_roques_autorisation.Update_roque_authorisation(move)


        self.next_color()
        self.move_LOG.append(move)

    def Undo_Move(self):
        if self.move_LOG :
            last_move = self.move_LOG[-1]
            if last_move.is_roque == False :
                self.board[last_move.end_row][last_move.end_col] = last_move.captured_piece  # on change la pièce d'arrivée
                self.board[last_move.start_row][last_move.start_col] = last_move.moved_piece
                if last_move.moved_piece == 'white_king' :
                    self.white_king_location = [last_move.start_row,last_move.start_col]
                if last_move.moved_piece == 'black_king' :
                    self.black_king_location = [last_move.start_row,last_move.start_col]
                self.next_color()
                self.move_LOG.pop(-1)
            elif last_move.is_roque :
                pass
                # undo roque
            else :
                print("no moves to undo, trait aux blancs!")


    def get_all_possibles_moves(self, player_colour):
        moves = []
        for rows in range(len(self.board)) : # Pour tout ligne
            for c in range(len(self.board[rows])) : #pour toute col in ligne
                # voir la couleur de la pièce
                piece_square = [rows, c]
                colour = self.get_piece_colour(piece_square)
                type = self.get_piece_type(piece_square)
                if colour == player_colour :
                    if type == "pawn" :
                        self.get_Pawn_moves(rows, c, moves, colour)
                    elif type == 'knight' :
                        self.get_Knight_moves(rows,c, moves, colour)
                    elif type == 'bishop':
                        self.get_Bishop_moves(rows,c,moves, colour)
                    elif type == 'rock' :
                        self.get_Rock_moves(rows, c, moves, colour)
                    elif type == 'queen' :
                        self.get_Queen_moves(rows, c, moves, colour)
                    elif type == 'king':
                        self.get_King_moves(rows, c, moves, colour)
                        self.get_Roque_Moves(rows, c, moves, colour)
                else :
                    pass


        return moves

    def get_all_moves_without_Roque(self, player_colour) :
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

    '''
         def in_check(self, op_moves):
            if self.colour_to_play == 'black' :
                return self.square_under_attack(self.white_king_location[0], self.white_king_location[1], op_moves)
            if self.colour_to_play == 'white' :
                return self.square_under_attack(self.black_king_location[0], self.black_king_location[1], op_moves)
        '''


    def square_under_attack(self, r ,c, color):
        op_color = self.opponent_colour(color)
        opponent_moves = self.get_all_moves_without_Roque(op_color)
        for move in opponent_moves :
            if move.end_row == r and move.end_col == c :
                return True
            else :
                pass
        return  False


    def get_Valid_moves(self, colour):
        legal_moves = []
        if colour == 'white'  :
            king_loc = self.white_king_location
        else :
            king_loc = self.black_king_location
        self.inCheck, self.clouage, self.checks = self.check_for_pins_and_checks(colour)
        if self.inCheck :# nous sommes en echec/ nous allons générer les réponses à l'échec
            print(len(self.checks))
            if len(self.checks) == 1 :
                legal_moves = self.get_all_possibles_moves(colour)
                check = self.checks[0]
                check_row = check[0]
                check_col = check[1]
                checking_piece = self.board[check_row][check_col]
                print(checking_piece)
                self.valid_squares = [] #cases sur lesquelles une pièce peut bouger pour empêcher l'échec
                if self.get_piece_type([check_row, check_col]) == 'knight' :#on ne peut pas bloquer le cavalier, il faut bouger le roi ou manger le cavalier
                    self.valid_squares.append((check_row, check_col))
                    # la seule pièce que l'on peut manger est le cavalier pour empêcher l'échec
                else :
                    for i in range(1, 8) :
                        valid_square = (king_loc[0] + i * check[2], king_loc[1] + i * check[3])
                        self.valid_squares.append(valid_square)
                        if valid_square[0] == check_row and valid_square[1] == check_col :
                            break
                #il faut se débarasser des moves qui n'enlèvent pas l'échec

                print(self.valid_squares)
                for i in range(len(legal_moves)- 1, -1, -1) : # on boucle à l'envers pour retirer les éléments d'une liste
                    if self.get_piece_type([legal_moves[i].start_row, legal_moves[i].start_col]) != 'king' : #si le move n'est pas un move du roi alors il doit bloquer ou manger la pièce, finir sur une valid square
                        if not (legal_moves[i].end_row, legal_moves[i].end_col) in self.valid_squares :
                            legal_moves.remove(legal_moves[i])
                    elif self.get_piece_type([legal_moves[i].start_row, legal_moves[i].start_col]) == 'king' :# enlève tous les moves du roi qui finissent sur les cases en echec
                        if (legal_moves[i].end_row, legal_moves[i].end_col) in self.valid_squares :
                            legal_moves.remove(legal_moves[i])
            else :  # double ou triple echecs on ne peut bloquer les pièce il faut boueger le roi
                legal_moves =self.get_King_moves(king_loc[0], king_loc[1], legal_moves, colour)
            pass
        else: #nous ne sommes pas en echecs nous pouvons analyser les moves possibles
            legal_moves = self.get_all_possibles_moves(colour) # on génère une fois tous les moves possibles
        """
        Pour vérifer que le roi ne se mette pas volontairement en échecs, il faut faire chaque move du Roi
        (on peut se le permettre c'est que 8 moves max)
        """
        for move in legal_moves :
            if self.get_piece_type([move.start_row, move.start_col]) == 'king' :
                print([move.start_row, move.start_col])
                if self.square_under_attack(move.end_row,move.end_col, self.colour_to_play) :
                    legal_moves.remove(move)
        if len(legal_moves) == 0 :
            if self.inCheck :
                self.checkmate = True
            else :
                self.pat = True


        return legal_moves

    # cet algorithme plus élégant ne recalcule plus tous le coups de l'adversaire pour voir si le roi est en echecs en traquant sa position
    # mais il part de la position du roi pour savoir si une pièce ennemi peut l'attaquer

    def check_for_pins_and_checks(self, colour):
        clouage = [] #contient les cases clouées par l'adversaire
        echecs = [] # contient les case avec les pièce attaquant le roi
        incheck = False #par défaut
        op_colour = self.opponent_colour(colour)
        if colour == 'white' :
            king_loc = self.white_king_location
        if colour == 'black' :
            king_loc = self.black_king_location

        # algorithme inverse des coups des pièce,on gère les cavaliers à part
        directions = ((0, -1), (0, +1), (+1, 0), (-1, 0),
                      (-1, -1), (-1, +1), (+1, -1), (+1, +1))
        for j in range(len(directions)) :
            possible_pin = ()
            d = directions[j]
            for i in range(1,8):  # pour chaque case on ajoute l'offset multiplié par l'itération => case finale du move
                check_row = king_loc[0] + i * d[0]
                check_col = king_loc[1] + i * d[1]
                if 0 < check_col < 8 and 0 <check_row < 8 :
                    check_piece = self.board[check_row][check_col]
                    if self.get_piece_colour([check_row, check_col]) == colour and\
                            self.get_piece_type([check_row,check_col]) != 'king': #pièce alliée clouage possible
                        if possible_pin == () :
                            possible_pin = (check_row, check_col, d[0], d[1])
                        else : # je suis protégé par deux pièces il n'y a pas de clouage
                            break
                    elif self.get_piece_colour([check_row, check_col]) == op_colour :# il y une pièece adverse vérifier l'échec
                        '''
                        condition complexe ici : nous sommes en echec si :
                        1) nous vérifions une colonne et la pièce est une tour
                        2) nous vérifions en diagonale et la pièce est un fou
                        3) nous vérifions les diagonales avant et la piièce est un pion 
                        4) la pièce est une dame (peut importe la direction)
                        5) il y a un roi deux case plus loin (pour empêcher le deplacement de notre roi sur une pièce controlé par un roi adverse)
                        '''
                        type = self.get_piece_type([check_row, check_col])
                        if( 0 <= j <=3 and type == 'rock') or \
                        (4 <= j <= 7 and type == 'bishop')or \
                        (type == 'queen' )or (i == 1 and type == 'king' )or \
                        (i == 1 and ((colour == 'white' and 4 <= j <= 5) or (colour == 'black' and 6 <= j <= 7) )):
                            if possible_pin == () : # il n'y a pas de pièce qui peut défendre le roi
                                incheck = True
                                echecs.append((check_row, check_col, d[0], d[1]))
                                break
                            else : # la pièce devient clouée
                                clouage.append(possible_pin)
                                break
                        else :#la pièce ne peut pas attaquer le roi ( par exemple la pièce est un cavalier adverse)
                            break
                else : #nous sommes sorti de l'échiquier
                    break
        #nous pouvons maintenant vérifier si les case de type cavaliers menace le roi
        knights_moves = ((-1, -2), (-1, +2), (+2, -1), (+2, +1),
                      (-2, -1), (-2, +1), (+1, -2), (+1, +2))
        for m in knights_moves :
            check_row = king_loc[0] + m[0]
            check_col = king_loc[1] + m[1]
            if 0 < check_col < 8 and 0 < check_row < 8:# on vérifie que l'on est sur le board
                if self.get_piece_type([check_row, check_col]) == 'knight' and\
                        self.get_piece_colour([check_row, check_col]) == op_colour:
                    incheck = True
                    print("echec par cavalier")
                    echecs.append((check_row, check_col, m[0], m[1]))
                    break
        return incheck, clouage, echecs

    def get_Roque_Moves(self, r, c, move, colour):
        '''
        Un Roque est un Move constitué de deux moves
        1) le roi se déplace de deux cases vers la Tour si aucune des case n'est en échec
        2) La tour se place derrière le Roi
        :return:
        '''
        if self.inCheck :
            return
        if colour == 'white' :
            if self.current_roques_autorisation.white_grand_roque :
                if self.board[r][c - 1] == 'Empty' and self.board[r][c - 2] == 'Empty':
                    if not (self.square_under_attack([r], [c - 1], self.colour_to_play) and self.square_under_attack([r],
                                                                                                                    [c],
                                                                                                                    self.colour_to_play)):
                        grand_roque = Moves([r, c], [r, c - 2], self.board)
                        grand_roque.is_roque = True
                        move.append(grand_roque)
            if self.current_roques_autorisation.white_petit_roque :
                if self.board[r][c + 1] == 'Empty' and self.board[r][c + 2] == 'Empty':
                    print("empty_check_passed")
                    # Trouver une manière la manière correcte d'ajoueter deux conditions if noot
                    if not (self.square_under_attack([r], [c + 1], self.colour_to_play) and   self.square_under_attack([r],
                                                                                                                      [c],
                                                                                                                    self.colour_to_play)):
                        petit_roque = Moves([r, c], [r, c + 2], self.board)
                        petit_roque.is_roque = True
                        move.append(petit_roque)

        elif colour == 'black' :
            if self.current_roques_autorisation.black_grand_roque :
                grand_roque = self.get_grand_roque_move(r, c)
                print(grand_roque)
                if grand_roque is not None :
                    move.append(grand_roque)
            if self.current_roques_autorisation.black_petit_roque :
                pass
        else :
            return


        #Grand Roque blanc :


    def get_grand_roque_move(self, r, c):
        if self.board[r][c - 1] == 'Empty' and self.board[r][c - 2] == 'Empty':
            if not self.square_under_attack([r],[c - 1], self.colour_to_play) and self.square_under_attack([r],[c],
                                                                                                          self.colour_to_play):
                grand_roque = Moves([r, c],[r, c - 2], self.board)
                grand_roque.is_roque = True
                return grand_roque


    '''
    Pieces moves by piece type, j'ai rajouté pour faire fonctionner l'algorithme complexe abordé par le tuto
    la variable piece_cloue = True/False
    
    '''
    def get_Pawn_moves(self, r, c , moves, colour) :
        # obtenir les coups possible du pion à la position r, c et les ajouter à moves
        piece_clouee = False
        pin_direction = ()
        for i in range(len(self.clouage)-1, -1, -1) :
            if self.clouage[i][0] == r and self.clouage[i][1] == c :
                piece_clouee = True
                pin_direction = (self.clouage[i][2], self.clouage[i][3])
                self.clouage.remove(self.clouage[i])
                break

        if colour == 'white':
            if self.board[r - 1][c] == 'Empty':
                if not piece_clouee or pin_direction == (0, -1) :
                    moves.append(Moves([r, c], [r - 1, c], self.board))  # on avance d'une case s'il n'y a pas de pièce
            if r == 6 and self.board[r - 2][c] == 'Empty' and self.board[r - 1][c] == 'Empty' :
                if not piece_clouee or pin_direction == (0, -1) :
                    moves.append(Moves([r, c], [r - 2, c], self.board))
            if c + 1 <= 7 :
                if self.get_piece_colour([r - 1,c + 1]) == 'black' :
                    if not piece_clouee or pin_direction == (-1, 1):
                        moves.append(Moves([r,c],[r -1,c+ 1], self.board))
            if c - 1 >= 0 :
                if self.get_piece_colour([r - 1,c - 1]) == 'black' :
                    if not piece_clouee or pin_direction == (-1, -1):
                        moves.append(Moves([r,c],[r -1,c- 1], self.board))
        if colour != 'white':
            if self.board[r+1][c] == 'Empty' :
                if not piece_clouee or pin_direction == (1, 0) :
                    moves.append(Moves([r, c], [r + 1, c], self.board))
            if r == 1 and self.board[r + 2][c] == 'Empty' :
                if not piece_clouee or pin_direction == (1, 0) :
                    moves.append(Moves([r, c], [r + 2, c], self.board))
            if c + 1 <= 7 :
                if self.get_piece_colour([r + 1,c + 1]) == 'white' :
                    if not piece_clouee or pin_direction == (1, 1):
                        moves.append(Moves([r,c],[r + 1,c+ 1], self.board))
            if c - 1 >= 0 :
                if self.get_piece_colour([r + 1,c - 1]) == 'white' :
                    if not piece_clouee or pin_direction == (1, -1):
                        moves.append(Moves([r,c],[r +1,c- 1], self.board))

    def get_Knight_moves(self, r, c , moves, colour) :
        piece_clouee = False
        pin_direction = ()
        for i in range(len(self.clouage) - 1, -1, -1):
            if self.clouage[i][0] == r and self.clouage[i][1] == c:
                piece_clouee = True
                pin_direction = (self.clouage[i][2], self.clouage[i][3])
                print(pin_direction)
                self.clouage.remove(self.clouage[i])
                break

        directions = ((-1, -2), (-1, +2), (+2, -1), (+2, +1),
                      (-2, -1), (-2, +1), (+1, -2), (+1, +2))
        for d in directions :
            if not piece_clouee :
                end_row = r + d[0]
                end_col = c + d[1]
                if 0 <= end_row < 8 and 0 <= end_col < 8 : # on est sur le board
                    if self.board[end_row][end_col] == 'Empty' :
                        moves.append(Moves([r, c], [end_row, end_col], self.board))
                    elif self.get_piece_colour([end_row, end_col]) != colour :
                        moves.append(Moves([r, c], [end_row, end_col], self.board))
                    else :
                        pass

    def get_Bishop_moves(self, r, c ,moves, colour):
        piece_clouee = False
        pin_direction = ()
        for i in range(len(self.clouage) - 1, -1, -1):
            if self.clouage[i][0] == r and self.clouage[i][1] == c:
                piece_clouee = True
                pin_direction = (self.clouage[i][2], self.clouage[i][3])
                print(pin_direction)
                self.clouage.remove(self.clouage[i])
                break

       # On cherche les coups possibles pour le bishop à la position self.board[r][c] si le move est autorisé, on ajoute à moves
        directions = ((-1, -1),(-1, +1),(+1, -1),(+1, +1))
        for d in directions :
            if not piece_clouee or pin_direction == d :
                for i in range(1, 8) : # pour chaque case on ajoute l'offset multiplié par l'itération => case finale du move
                    end_row = r + i * d[0]
                    end_col = c + i * d[1]
                    if 8 > end_col >= 0 and 8 > end_row >= 0 :  # On est sur l'echiquier
                        end_piece = self.board[end_row][end_col]
                        if end_piece == 'Empty' : #case vide
                            moves.append(Moves([r, c],[end_row, end_col], self.board))
                        elif self.get_piece_colour([end_row, end_col]) != colour : #pièce adverse
                            moves.append(Moves([r, c],[end_row, end_col], self.board))
                            break #on ne peut pas aller plus loin dans cette direction, break casse la loop direction
                        else : # le dernier cas est une pièce alliée
                            break
                    else :  # on sort du board
                        break

    def get_Rock_moves(self, r, c, moves, colour):
        piece_clouee = False
        pin_direction = ()
        for i in range(len(self.clouage) - 1, -1, -1):
            if self.clouage[i][0] == r and self.clouage[i][1] == c:
                piece_clouee = True
                pin_direction = (self.clouage[i][2], self.clouage[i][3])
                print(pin_direction)
                self.clouage.remove(self.clouage[i])
                break
        # même fonctionnement que pour le fou mais on change les directions
        directions = ((0, -1), (0, +1), (+1, 0), (-1, 0))
        for d in directions:
            if not piece_clouee or pin_direction == d :
                for i in range(1, 8):  # pour chaque case on ajoute l'offset multiplié par l'itération => case finale du move
                    end_row = r + i * d[0]
                    end_col = c + i * d[1]
                    if 8 > end_col >= 0 and 8 > end_row >= 0:  # On est sur l'echiquier
                        end_piece = self.board[end_row][end_col]

                        if end_piece == 'Empty':  # case vide
                            moves.append(Moves([r, c], [end_row, end_col], self.board))

                        elif self.get_piece_colour([end_row, end_col]) != colour:  # pièce adverse
                            moves.append(Moves([r, c], [end_row, end_col], self.board))
                            break  # on ne peut pas aller plus loin dans cette direction, break casse la loop direction
                        elif self.get_piece_colour([end_row, end_col]) != colour:  # le dernier cas est une pièce alliée
                            break
                        else :
                            break

                    else:  # on sort du board
                        break

    def get_Queen_moves(self, r, c, moves, colour ):
        piece_clouee = False
        pin_direction = ()
        for i in range(len(self.clouage) - 1, -1, -1):
            if self.clouage[i][0] == r and self.clouage[i][1] == c:
                piece_clouee = True
                pin_direction = (self.clouage[i][2], self.clouage[i][3])
                print(pin_direction)
                self.clouage.remove(self.clouage[i])
                break
        #même fonctionnement que pour la tour mais on fusionne les directions du fou et de la tour
        directions = ((0, -1), (0, +1), (+1, 0), (-1, 0),
                      (-1, -1),(-1, +1),(+1, -1),(+1, +1))
        for d in directions:
            if not piece_clouee or pin_direction == d :
                for i in range(1,
                               8):  # pour chaque case on ajoute l'offset multiplié par l'itération => case finale du move
                    end_row = r + i * d[0]
                    end_col = c + i * d[1]
                    if 8 > end_col >= 0 and 8 > end_row >= 0:  # On est sur l'echiquier
                        end_piece = self.board[end_row][end_col]

                        if end_piece == 'Empty':  # case vide
                            moves.append(Moves([r, c], [end_row, end_col], self.board))

                        elif self.get_piece_colour([end_row , end_col]) != colour :  # pièce adverse
                            moves.append(Moves([r, c], [end_row, end_col], self.board))


                            break  # on ne peut pas aller plus loin dans cette direction, break casse la loop direction
                        else:  # le dernier cas est une pièce alliée
                            break
                    else:  # on sort du board
                        break

    def get_King_moves(self, r, c, moves, colour):
        directions = ((0, -1), (0, +1), (+1, 0), (-1, 0),
                      (-1, -1), (-1, +1), (+1, -1), (+1, +1))
        for d in directions:
            end_col = c + d[1]
            end_row = r + d[0]
            if 0 <= end_row <8 and 0 <= end_col < 8 :
                if self.board[end_row][end_col] == 'Empty' :
                    moves.append(Moves([r,c],[end_row,end_col], self.board))
                elif self.get_piece_colour([end_row,end_col]) != colour :
                    moves.append(Moves([r,c],[end_row,end_col], self.board))
                else :
                    pass
            else :
                pass




        #check if king is attacked
        #check if castling cases are attacked
        # check if tower and king have moved
        #vérifier dans le log si aucun move n'est parti de la case du roi ou de la tour
        # check that castling cases are empty
        # le roque contient deux moves"""
'''

'''

class Moves() :
    # contient les éléments d'un seul coup d'échec (pièces de départ et d'arrivée + le bord)
    ranks_to_row = {"1" : 7, "2" : 6, "3" : 5, "4" : 4 , "5" : 3,
                    "6" : 2, "7" : 1, "8" : 0}
    row_to_ranks = {v : k for k, v in ranks_to_row.items()}
    col_to_letter = {"h" : 7, "g" : 6, "f" : 5, "e" : 4 , "d" : 3,
                    "c" : 2, "b" : 1, "a" : 0}
    letter_to_col = {v: k for k, v in col_to_letter.items()}


    def __init__(self, start_sq, end_sq, board):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.moved_piece = board[self.start_row][self.start_col]
        self.captured_piece = board[self.end_row][self.end_col]
        self.moveID = self.start_row * 1000 + self.start_col * 100 + self.end_col * 10 + self.end_row
        self.is_roque = False

    '''
    Nous devons comparer les les Moves générés par les clics et les moves autorisés générés par le jeu. 
    Comme nous devons comparer deux moves, nous devons comparer un élément qui serra commun aux mêmes moves.
    Il s'agit du move ID 
    
    __eq__(self, other) est une fonction automatique, elle est appellée à chaque utilisation de == (eq) et override
    lorsque les deux moves sont comparés, si ils possèdent les même ID l'opérateur == renvoie TRUE 
    '''

#se renseigner sur la fonciton __eq__(self, other)
    def __eq__(self, other):
        if isinstance(other, Moves) :
            return self.moveID == other.moveID
        return False

    def get_notation(self):
        return self.getLetterRow(self.start_row, self.start_col)  + self.getLetterRow(self.end_row, self.end_col)


    def getLetterRow(self, r, c):
        return self.letter_to_col[c] + self.row_to_ranks[r]

    def get_cases(self):
        cases = [(self.start_row,self.start_col),(self.end_row,self.end_col)]
        return cases


class Roque_Autorisation :
    """
    Cette classe permet de traquer les autorisations de roques pour les deux couleurs et les deux types
    de roques (grand roque, petit roque) :
    -le roi ne peut plus roquer des deux côtés si il a bougé
    -le roi ne peut plus roquer d'un côté si la tour de ce côté a roqué

    """
    def __init__(self, white_grand_roque, white_petit_roque, black_petit_roque, black_grand_roque ) :
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
        if move.moved_piece == 'black_king' :
            self.black_grand_roque = False
            self.black_petit_roque = False
        elif move.moved_piece == 'white_king' :
            self.white_grand_roque = False
            self.white_petit_roque = False

        elif move.moved_piece == 'white_rock' :
            if (move.start_row, move.start_col) == (7, 0) :
                self.white_grand_roque = False
            if (move.start_row, move.start_col) == (7, 7):
                self.white_petit_roque = False

        elif move.moved_piece == 'black_rock' :
            if (move.start_row, move.start_col) == (0, 0) :
                self.black_grand_roque = False
            if (move.start_row, move.start_col) == (0, 7) :
                self.black_petit_roque = False







