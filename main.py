import math
import pygame
import chess_engine
import sys, time


pygame.font.init()
board_offset = (64, 128)
board_position= (576, 640 )
print(board_position)
FPS = 60
class Framerate_exemple():
    def __init__(self):
        self.previousTime = time.time()
        """
        Il faut mettre self.now, self.dt et self.previousTime dans la boucle self.Run() du jeu
        """
        self.now = time.time() # on génère le temps de la frame
        self.dt = self.now - self.previousTime #on calcule le delta T de l'ancienne frame
        self.previousTime = self.now # le temps actuel est le temps de l'ancienne frame
        self.clock = pygame.time.Clock()
        """
        Tous les concepts frames dépendants doivent être multipliés par self.dt (animation, vélocité etc.) et le frameRATE
        comme le delta normal est 1/60 * 60, lorsque dt augmente l'animation ou la vélocité compense la perte de framerate
        """
        self.clock.get_fps()



class Game() :
    """
    Taille finale de l'application (704,768), taille de l'échiquier (512,512)


    """
    def __init__(self):


        self.author = "Baptiste Fraboul"  # TODO: tu utilises jamais cette variable. C'est à retirer à mon avis.
        self.name = "Chess "
        self.window_size = (704,768)
        self.window = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Chess game!")
        self.running = True
        self.clock = pygame.time.Clock()
        """
        Font section
        """
        self.Arial_font = pygame.font.Font('fonts/ARIALN.TTF',16)


        """
        Pygame.Color section
        """
        self.default_color = pygame.Color((61,61,61))
        self.error_color = pygame.Color((136,0,21))

        self.board = chess_engine.ChessBoard()
        self.board.set_starting_position()

        # gestion des moves légaux
        self.Valid_moves = self.board.get_Valid_moves(self.board.colour_to_play)
        self.move_made = False # Pour éviter de regénérer tous les moves à chaque frame, regénéer les nouveaux valid_move lorsque le move a été fait

        self.right_clicking = False
        self.mx , self.my = pygame.mouse.get_pos()

        # self.clicks contient une paire de case à comparer pour générer les coups d'échecs

        self.player_clicks = []
        self.selected_case = ()
        pygame.mouse.set_cursor(pygame.cursors.diamond)

    def final_screen(self):
        # TODO: c'est une méthode (ie un truc qui fait quelque chose) mais son
        #  nom ne dit rien sur ce qu'elle fait. Ça devrait pas plutôt s'appeler
        #  display_game_end_screen? J'ai été obligé de lire le contenu de la
        #  fonction pour comprendre ce qu'elle fait.
        running = True
        window = pygame.display.set_mode(self.window_size)
        message_rect = pygame.Rect((10,256),(64, 256))
        if self.board.pat :
            text = 'Stalemate, no one won the game'
        if self.board.checkmate :
            winner = self.board.opponent_colour(self.board.colour_to_play)
            text = winner + " have won the game by checkmate"
        message = self.Arial_font.render(text,True,'Red',(0,0,0))
        while running :
            for event in pygame.event.get():
                if event.type == pygame.K_ESCAPE :
                    running = False
                    sys.exit()
            window.blit(message,message_rect)

    def inside_board (self,x, y) :
        # TODO: Ça devrait plutôt s'appeler is_inside_board non?
        if 64 <= x <= 576 and 128 <= y <= 640 :
            return True
        else :
            return False
    '''
    Permet la gestion dela boucle d'events, tout ce qui est input du joueur est géré ici
    '''
    def click_handling(self, event):
        # TODO: Ça devrait plutôt s'appeler handle_click_event non?
        """
        gestion des clics de la souris
        """

        if event.type == pygame.MOUSEBUTTONDOWN:
            # clic droit détecté
            #on vérifie que le click est bien sur le board de l'échiquier
            if self.inside_board(self.mx, self.my) :
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

                            move = chess_engine.Moves(self.player_clicks[0], self.player_clicks[1], self.board.board)

                            if move in self.Valid_moves:
                                self.board.Make_Move(move)
                                self.move_made = True
                                self.player_clicks = []  # deselect
                                self.selected_case = ()


                            else:
                                self.player_clicks = []  # deselect
                                self.selected_case = ()


                        else:
                            self.player_clicks = []  # deselect
                            self.selected_case = ()

                if self.move_made:
                    self.Valid_moves = self.board.get_Valid_moves(self.board.colour_to_play)
                    self.move_made = False
            else :
                print("Outside gameboard")


    def events(self):
        # TODO: Ça devrait plutôt s'appeler handle_events. Là juste events,
        #  c'est pas clair.

        self.right_clicking = False
        self.mx, self.my = pygame.mouse.get_pos()
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                self.running = False
                # TODO: pourquoi un sys.exit() et pas juste un return? Là tu
                #  forces python à s'arrêter.
                sys.exit()

            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_SPACE :
                    for moves_in_LOG in self.board.move_LOG :
                        print(moves_in_LOG.get_notation())

                if event.key == pygame.K_a :
                    self.board.Undo_Move()
                    self.Valid_moves= self.board.get_Valid_moves(self.board.colour_to_play)

                if event.key == pygame.K_b :
                    self.board.get_Valid_moves(self.board.colour_to_play)

            self.click_handling(event)


    '''
    La boucle update nous servira à faire des mise à jour automatique en fonction des changement d'état
    '''
    def update(self):
        pass

    '''
    La boucle display nous permet la gestion des élémetns graphique et des layers d'affichage
    '''

    def display(self):
        """
        couleur du fond par défaut, gris Ensi
        """
        self.window.fill(self.default_color)

        self.window.blit(pygame.image.load("assets/board/export/Application_bg.png"),(0,0))
        self.board.draw(self.window)
        self.board.draw_pieces(self.window)

        if self.player_clicks != [] :
            self.board.draw_moves(self.window,self.Valid_moves,self.player_clicks[0])
        if self.board.checkmate or self.board.pat :
            self.running = False
            sys.exit()
            self.final_screen()  # TODO: Cette fonction sera jamais appeler.
            # Pareil pas besoin d'un sys.exit ici.


        pygame.display.flip()



    def run(self):
        while self.running :
            self.events()
            self.update()
            self.display()
            self.clock.tick(60)

# TODO: tu devrais mettre ça dans un main:
#  if __name__ == "__main__":
#      test = Game()
#      test.run()

test = Game()
test.run()