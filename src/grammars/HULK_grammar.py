from utils.pycompiler import Grammar
from ast_nodes.hulk_ast_nodes import *


def get_hulk_grammar():
    G = Grammar()
    
    expr = G.NonTerminal('<expr>', startSymbol=True)
    expr_list, stringify, term, factor, atom, func_call, arg_list = G.NonTerminals('<expr-list> <stringify> <term> <factor> <atom> <func-call> <arg-list>')
    
    sum, sub, mul, div, pow1, pow2, num, id, opar, cpar, ocurl, ccurl, coma, semicolon, at = G.Terminals('+ - * / ^ ** num id ( ) { } , ; @')
    
    expr %= ocurl + expr_list + ccurl, lambda h, s: BlockExprNode(s[2]), None, None, None
    expr %= stringify + at + expr, lambda h, s: BinaryOperationNode(s[1], s[3], s[2]), None, None, None
    expr %= stringify, lambda h, s: s[1], None
    
    stringify %= term + sum + expr, lambda h, s: BinaryOperationNode(s[1], s[3], s[2]), None, None, None
    stringify %= term + sub + expr, lambda h, s: BinaryOperationNode(s[1], s[3], s[2]), None, None, None
    stringify %= term, lambda h, s: s[1], None
    
    expr_list %= expr + semicolon + expr_list, lambda h, s: [s[1]] + s[3], None, None, None
    expr_list %= expr, lambda h, s: [s[1]], None
    
    term %= factor + mul + term, lambda h, s: BinaryOperationNode(s[1], s[3], s[2]), None, None, None
    term %= factor + div + term, lambda h, s: BinaryOperationNode(s[1], s[3], s[2]), None, None, None
    term %= factor, lambda h, s: s[1], None
    
    factor %= atom + pow1 + factor, lambda h, s: BinaryOperationNode(s[1], s[3], s[2]), None, None, None
    factor %= atom + pow2 + factor, lambda h, s: BinaryOperationNode(s[1], s[3], s[2]), None, None, None
    factor %= atom, lambda h, s: s[1], None
    
    atom %= num, lambda h, s: ConstantNumberNode(s[1]), None
    atom %= id, lambda h, s: VariableNode(s[1]), None
    atom %= func_call, lambda h, s: s[1], None
    atom %= opar + expr + cpar, lambda h, s: s[2], None, None, None
    
    func_call %= id + opar + arg_list + cpar, lambda h, s: FuncCallNode(s[1], s[3]), None, None, None, None
    
    arg_list %= expr + coma + arg_list, lambda h, s: [s[1]] + s[3], None, None, None
    arg_list %= expr, lambda h, s: [s[1]], None
    
    return G
