import chess_engine as engine
from stockfish import Stockfish

class Chess_Ai:
    def __init__(self):
        self.stockfish  =  Stockfish(path="D:/Stockfish/stockfish_14.1_win_x64_popcnt.exe")

    def do_best_move(self,fen_notation):
        self.stockfish.set_fen_position(fen_notation)
        notation = self.stockfish.get_best_move()
        move = engine.algebric_to_Move(notation)
        return move
