from  utils.pycompiler import Grammar
from  ast_nodes.regex_nodes import *


G = Grammar()

init = G.NonTerminal('<init>', startSymbol=True)

union, concat, kleene, atom = G.NonTerminals('<union> <concat> <kleene> <atom>')

pipe, star, opar, cpar, symbol = G.Terminals('| * ( ) symbol')

init %= union, lambda h, s: s[1], None

union %= union + pipe + concat, lambda h, s: UnionNode(s[1], s[3]), None, None, None

union %= concat, lambda h, s: s[1], None

concat %= concat + kleene, lambda h, s: ConcatNode(s[1], s[2]), None, None

concat %= kleene, lambda h, s: s[1], None

kleene %= atom + star, lambda h, s: ClosureNode(s[1]), None, None

kleene %= atom, lambda h,s: s[1], None

atom %= symbol, lambda h, s: SymbolNode(s[1]), None

atom %= opar + init + cpar, lambda h, s: s[2], None, None, None

