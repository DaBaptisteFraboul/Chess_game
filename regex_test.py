import re

letter_to_col = {"h": 7, "g": 6, "f": 5, "e": 4, "d": 3,
                     "c": 2, "b": 1, "a": 0}
row_to_rank = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3,
                "6": 2, "7": 1, "8": 0}
regex_pattern = r"([a-h])([1-8])([a-h])([1-8])"
move = ("e2e4")

pattern = r"([a-h])([1-8])([a-h])([1-8])"

results = re.findall(pattern, move)[0]
start_col = letter_to_col[results[0]]
print(start_col)