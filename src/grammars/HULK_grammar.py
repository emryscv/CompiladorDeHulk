from ast_nodes.hulk_ast_nodes import *


def get_hulk_grammar():
    G = Grammar()
    
    expr = G.NonTerminal('<expr>', startSymbol=True)
    expr_list, stringify, term, factor, atom, func_call, arg_list, func_def, arg_def_list, func_body, var_def, boolean_expr, boolean_term = G.NonTerminals('<expr-list> <stringify> <term> <factor> <atom> <func-call> <arg-list> <func-def> <arg-def-list> <func-body> <var-def> <boolean-expr> <boolean-term>')
    
    sum, sub, mul, div, pow1, pow2, num, id, opar, cpar, ocurl, ccurl, coma, semicolon, at, function, arrow, let, in_token, asign_equal, asign, if_token, else_token, and_token, or_token, lower, greater, lower_equal, greater_equal, equal, diferent, true, false, while_token, for_token = G.Terminals('+ - * / ^ ** num id ( ) { } , ; @ function => let in = := if else & | < > <= >= == != true false while for')
    
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
    
    func_def %= function + id + opar + arg_def_list + cpar + func_body, lambda h , s: FuncDefNode(s[2], s[4], s[6]), None, None, None, None, None, None
    arg_def_list %= id + coma + arg_def_list, lambda h , s: [s[1]] + s[3], None, None, None
    arg_def_list %= id , lambda h ,s: [s[1]], None
    arg_def_list %= G.Epsilon, lambda h , s: [], None
    func_body %= arrow + expr + semicolon, lambda h ,s: s[2], None, None, None
    func_body %= ocurl + expr_list + ccurl, lambda h, s: BlockExprNode(s[2]), None, None, None
    
    ###variables###
    
    
    expr %= let + var_def + in_token + expr, lambda h, s: LetInNode(s[2], s[4]), None, None, None
    expr %= id + asign + expr, lambda h, s: VarReAsignNode(s[1], s[3]), None, None, None
    
    var_def %= id + asign_equal + expr + coma + var_def , lambda h , s: [VarDefNode(s[1], s[3])] + s[5]
    var_def %= id + asign_equal + expr, lambda h , s: [VarDefNode(s[1], s[3])]
    
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
    
    return G
