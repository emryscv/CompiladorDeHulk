from src.utils.pycompiler import Grammar
from src.ast_nodes.regex_nodes import *


def get_hulk_grammar():
    G = Grammar()
    
    expr = G.NonTerminal('<expr>', startSymbol=True)
    expr_list, term, factor, atom, func_call, arg_list = G.NonTerminals('<expr-list> <term> <factor> <atom> <func-call> <arg-list>')
    
    sum, sub, mul, div, pow1, pow2, num, id, opar, cpar, ocurl, ccurl, coma, semicolon = G.Terminals('+ - * / ^ ** num id ( ) { } , ;')
    
    expr %= ocurl + expr_list + ccurl, None, None, None, None
    expr %= term + sum + expr, None, None, None, None
    expr %= term + sub + expr, None, None, None, None
    expr %= term, None, None
    
    expr_list %= expr + semicolon + expr_list, None, None, None, None
    expr_list %= expr, None, None
    
    term %= factor + mul + term, None, None, None, None
    term %= factor + div + term, None, None, None, None
    term %= factor, None, None
    
    factor %= atom + pow1 + factor, None, None, None, None
    factor %= atom + pow2 + factor, None, None, None, None
    factor %= atom, None, None
    
    atom %= num, None, None
    atom %= id, None, None
    atom %= func_call, None, None
    atom %= opar + expr + cpar, None, None, None, None
    
    func_call %= id + opar + arg_list + cpar, None, None, None, None, None
    
    arg_list %= expr + coma + arg_list, None, None, None, None
    arg_list %= expr, None, None