from stockfish import Stockfish

stockfish = Stockfish(path="stockfish_14.1_win_x64_popcnt/stockfish_14.1_win_x64_popcnt.exe")

def computer_move() :
    AI_move = stockfish.get_best_move()
    print(AI_move)

stockfish.set_fen_position("rnbqkbnr/ppp1pppp/8/3p4/4P3/3B4/PPPP1PPP/RNBQK1NR b KQkq - 3 1")
computer_move()