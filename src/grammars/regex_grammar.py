from src.utils.pycompiler import Grammar
from src.ast_nodes.regex_nodes import *

def get_regex_grammar():
    G = Grammar()

    init = G.NonTerminal('<init>', startSymbol=True)

    union, concat, kleene = G.NonTerminal('<union>', '<concat>', '<kleene>')

    pipe, star, opar, cpar, symbol = G.Terminals('| * ( ) symbol')

    init %= union

    union %= union + pipe + concat

    union %= concat

    concat %= concat + kleene

    concat %= kleene

    kleene %= kleene + star

    kleene %= symbol

    kleene %= opar + init + cpar
