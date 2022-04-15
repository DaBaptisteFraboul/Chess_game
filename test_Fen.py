import re

Fen = "r1bqkb1r/1p3ppp/2n1pn2/1pp5/3pP3/3P1N2/PPPBBPPP/R2Q1RK1 w kq - 0 8"

regex_pattern = r"[rwqbkpnRQBKPN0-8-]+"
result = re.findall(regex_pattern, Fen)

Fen_table = {
    "r":"black_tower",
    "q":"black_queen",
    "k":"black_king",
    "p":"black_pawn",
    "n":"black_knight",
    "b":"black_bishop",
    "R":"white_tower",
    "Q":"white_queen",
    "K":"white_king",
    "P":"white_pawn",
    "N":"white_knight",
    "B":"white_bishop",
}
board =[
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
def translate_FEN(FEN) :
    regex_pattern = r"[rwqbkpnRQBKPN0-8-]+"
    parsing = re.findall(regex_pattern, Fen)
    for row in range (0, 8) :
        col = 0
        for element in parsing[row] :
            if not element.isdigit():
                board[row][col] = Fen_table[element]
                col += 1
            else :
                col += int(element)
            print(col)

    print(board)

translate_FEN(Fen)
