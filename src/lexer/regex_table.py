from  grammars.HULK_grammar import *

nonzero_digits = '|'.join(str(n) for n in range(1, 10))
digits = '|'.join(str(n) for n in range(10))
lower_letters = '|'.join(chr(n) for n in range(ord('a'), ord('z') + 1))
upper_letters = '|'.join(chr(n) for n in range(ord('A'), ord('Z') + 1))

IDENTIFIER = f"({lower_letters}{upper_letters}|_)({lower_letters}{upper_letters}{digits}|_)*"
NUMBER = f'({nonzero_digits}{digits})*'
regex_table = [
    ('space', ' '),
    (let, 'let'),
    (in_token, 'in'),
    (asign_equal, '='),
    (num, NUMBER),
    (id, IDENTIFIER)
]