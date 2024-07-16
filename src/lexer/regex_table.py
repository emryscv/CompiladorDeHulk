import string
from  grammars.HULK_grammar import *

regex_grammar_characters = ['"', '|', '*', '(', ')', '\\']
regex_grammar_characters_scapes = '\\\"|\\||\\*|\\(|\\)'

nonzero_digits = '|'.join(str(n) for n in range(1, 10))
digits = '|'.join(str(n) for n in range(10))
lower_letters = '|'.join(chr(n) for n in range(ord('a'), ord('z') + 1))
upper_letters = '|'.join(chr(n) for n in range(ord('A'), ord('Z') + 1))
all_characters = '|'.join(n for n in string.printable if not n in regex_grammar_characters)

IDENTIFIER = f"({lower_letters}|{upper_letters}|_)({upper_letters}|{lower_letters}|{digits}|_)*"
NUMBER = f'({nonzero_digits})({digits})*|({nonzero_digits})({digits})*.({digits})*|0.({digits})*|0'
SPACE_CHARACTERS = f'( |\n|\t)'
STRING = f'"({all_characters}|{regex_grammar_characters_scapes})*"'

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
    (extends, 'extends'), 
    (and_token, '&'), 
    (or_token, '\\|'),
    (sum, '+'), 
    (sub, '-'),
    (mul, '\\*'), 
    (div, '/'), 
    (pow1, '^'), 
    (mod, '%'),
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
    (string_literal, STRING),
    ('space', SPACE_CHARACTERS)
]
