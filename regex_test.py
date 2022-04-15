import re

letter_to_col = {"h": 7, "g": 6, "f": 5, "e": 4, "d": 3,
                     "c": 2, "b": 1, "a": 0}
row_to_rank = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3,
                "6": 2, "7": 1, "8": 0}

Fen = "r1bqkb1r/1p3ppp/2n1pn2/1pp5/3pP3/3P1N2/PPPBBPPP/R2Q1RK1 w kq - 0 8"

regex_pattern = r"[rwqbkpnRQBKPN0-8-]+"
result = re.findall(regex_pattern, Fen)

print(result)