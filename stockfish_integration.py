import chess_engine as engine
from stockfish import Stockfish


stockfish = Stockfish(path="D:/Stockfish/stockfish_14.1_win_x64_popcnt.exe")


def do_best_move( fen_notation, board):
    stockfish.set_fen_position(fen_notation)
    notation = stockfish.get_best_move()
    move = engine.algebric_to_Move(notation, board)
    return move


