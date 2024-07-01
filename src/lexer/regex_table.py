from  grammars.HULK_grammar import *

nonzero_digits = '|'.join(str(n) for n in range(1, 10))
digits = '|'.join(str(n) for n in range(10))
lower_letters = '|'.join(chr(n) for n in range(ord('a'), ord('z') + 1))
upper_letters = '|'.join(chr(n) for n in range(ord('A'), ord('Z') + 1))

IDENTIFIER = f"({lower_letters}{upper_letters}|_)({lower_letters}{upper_letters}{digits}|_)*"
NUMBER = f'({nonzero_digits}{digits})*'
SPACE_CHARACTERS = f'( |\n|\t)'
regex_table = [
    (let, 'let'),
    (if_token, 'if' ), 
    (elif_token, 'elif'), 
    (else_token, 'else'), 
    (function, 'function'),
    (true, 'true'), 
    (false, 'false'), 
    (while_token, 'while'), 
    (for_token, 'for'), 
    (type_token, 'type'), 
    (inherits, 'inherits'), 
    (new, 'new'), 
    (protocol, 'protocol'), 
    (and_token, '&'), 
    (or_token, '\\|'),
    (sum, '+'), 
    (sub, '-'),
    (mul, '\\*'), 
    (div, '/'), 
    (pow1, '^'), 
    (pow2, '\\*\\*'), 
    (opar, '\\('), 
    (cpar, '\\)'), 
    (ocurl, '{'), 
    (ccurl, '}'),
    (lower, '<'), 
    (greater, '>'), 
    (lower_equal, '<='), 
    (greater_equal, '>='), 
    (diferent, '!='),
    (dot, '.'),
    (coma, ','),  
    (at, '@'), 
    (double_at, '@@'), 
    (colon, ':'),
    (asign, ':='), 
    (in_token, 'in'),
    (asign_equal, '='),
    (equal, '=='), 
    (arrow, '=>'),  
    (semicolon, ';'),
    (num, NUMBER),
    (id, IDENTIFIER),
    ('space', SPACE_CHARACTERS)
]
