from src.utils.pycompiler import Grammar
from src.ast_nodes.regex_nodes import *


def get_regex_grammar():
    G = Grammar()

    init = G.NonTerminal('<init>', startSymbol=True)

    union, concat, kleene, atom, literal = G.NonTerminals('<union>', '<concat>', '<kleene>', '<atom>')

    pipe, star, opar, cpar, symbol = G.Terminals('| * ( ) symbol')

    init %= union, lambda h, s: s[1], None

    union %= union + pipe + concat, lambda h, s: UnionNode(s[1], s[2]), None, None

    union %= concat, lambda h, s: s[1], None

    concat %= concat + kleene, lambda h, s: ConcatNode(s[1], s[2]), None, None

    concat %= kleene, lambda h, s: s[1], None

    kleene %= atom + star, lambda h, s: ClosureNode(s[1]), None, None

    kleene %= symbol, lambda h, s: SymbolNode(s[1]), None

    kleene %= opar + init + cpar, lambda h, s: s[2], None, None, None

    return G
