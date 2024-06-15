from utils.pycompiler import Grammar
from ast_nodes.hulk_ast_nodes import *


def get_hulk_grammar():
    G = Grammar()
    
    expr = G.NonTerminal('<expr>', startSymbol=True)
    expr_list, stringify, term, factor, atom, func_call, arg_list, func_dec, arg_dec_list, func_body, var_dec, boolean_expr, boolean_term, type_dec, type_body, type_body_stat, optional_args, optional_inherits, optional_inherits_args = G.NonTerminals('<expr-list> <stringify> <term> <factor> <atom> <func-call> <arg-list> <func-dec> <arg-dec-list> <func-body> <var-dec> <boolean-expr> <boolean-term> <type-dec> <type-body> <type-body-stat> <optional-args> <optional-inherits> <optional-inherits-args>')
    
    sum, sub, mul, div, pow1, pow2, num, id, opar, cpar, ocurl, ccurl, coma, semicolon, at, function, arrow, let, in_token, asign_equal, asign, if_token, else_token, and_token, or_token, lower, greater, lower_equal, greater_equal, equal, diferent, true, false, while_token, for_token, type_token, inherits, new = G.Terminals('+ - * / ^ ** num id ( ) { } , ; @ function => let in = := if else & | < > <= >= == != true false while for type inherits new')
    
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
    
    atom %= num, lambda h, s: ConstantNode(s[1]), None
    atom %= id, lambda h, s: VariableNode(s[1]), None
    atom %= func_call, lambda h, s: s[1], None
    atom %= opar + expr + cpar, lambda h, s: s[2], None, None, None
    
    func_call %= id + opar + arg_list + cpar, lambda h, s: FuncCallNode(s[1], s[3]), None, None, None, None
    
    arg_list %= expr + coma + arg_list, lambda h, s: [s[1]] + s[3], None, None, None
    arg_list %= expr, lambda h, s: [s[1]], None
    
    ###functions###
    func_dec %= function + id + opar + arg_dec_list + cpar + func_body, None, None, None, None, None, None, None
    
    arg_dec_list %= id + coma + arg_dec_list, None, None, None, None
    arg_dec_list %= id 
    
    func_body %= arrow + expr + semicolon, None, None, None, None
    func_body %= ocurl + expr_list + ccurl, None, None, None, None
    
    ###variables###
    expr %= let + var_dec + in_token + expr, None, None, None, None
    expr %= id + asign + expr
    
    var_dec %= id + asign_equal + expr + coma + var_dec
    var_dec %= id + asign_equal + expr
    
    ### if - else###
    expr %= if_token + opar + boolean_expr + cpar + expr + else_token + expr
    
    boolean_expr %= boolean_term + and_token + boolean_expr
    boolean_expr %= boolean_term + or_token + boolean_expr
    boolean_expr %= boolean_term
    
    boolean_term %= expr + lower + expr, None, None, None, None
    boolean_term %= expr + greater + expr, None, None, None, None
    boolean_term %= expr + lower_equal + expr, None, None, None, None
    boolean_term %= expr + greater_equal + expr, None, None, None, None
    boolean_term %= expr + equal + expr, None, None, None, None
    boolean_term %= expr + diferent + expr, None, None, None, None
    boolean_term %= true, None, None
    boolean_term %= false, None, None
    boolean_term %= id, None, None
    
    ###loops###
    expr %= while_token + opar + boolean_expr + cpar + expr, None, None, None, None, None, None
    expr %= for_token + opar + id + in_token + expr + cpar + expr, None, None, None, None, None, None, None, None
    
    ###types###
    type_dec %= type_token + id + optional_args +  ocurl + type_body + ccurl, None, None, None, None, None, None, None
    
    optional_args %= opar + arg_dec_list + cpar, None, None, None, None
    optional_args %= G.Epsilon, None, None
    
    optional_inherits %= inherits + id + optional_inherits_args, None, None, None, None
    optional_inherits %= G.Epsilon, None, None
    
    optional_inherits_args %= opar + arg_list + cpar, None, None, None, None
    optional_inherits_args %= G.Epsilon, None, None
    
    
    type_body %= type_body_stat + semicolon + type_body, None, None, None, None,
    type_body %= type_body_stat + semicolon, None, None, None
    
    type_body_stat %= id + asign_equal + expr, None, None, None, None
    type_body_stat %= id + opar + arg_dec_list + cpar + func_body, None, None, None, None, None, None
    
    expr %= new + id + opar + arg_list + cpar, None, None, None, None, None, None
    
    return G
