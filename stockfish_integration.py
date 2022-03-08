import math

from stockfish import Stockfish

stockfish = Stockfish(path="D:/Stockfish/stockfish_14.1_win_x64_popcnt.exe")

stockfish.set_fen_position("2r3k1/1p2Qpp1/p2Pq3/P1p5/2P4P/4p3/6P1/4R2K w - - 1 34")

best_move = stockfish.get_best_move()
print(3 / 2)
print(math.trunc(7/2))
print(best_move)