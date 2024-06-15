from ast_nodes.hulk_ast_nodes import *


def get_hulk_grammar():
    G = Grammar()
    
    expr = G.NonTerminal('<expr>', startSymbol=True)
    
    expr_list, stringify, term, factor, atom, func_call, arg_list, func_dec, arg_dec_list, func_body, var_dec, elif_expr, boolean_expr, boolean_term, type_dec, type_body, type_body_stat, optional_args, optional_inherits, optional_inherits_args = G.NonTerminals('<expr-list> <stringify> <term> <factor> <atom> <func-call> <arg-list> <func-dec> <arg-dec-list> <func-body> <var-dec> <elif_expr> <boolean-expr> <boolean-term> <type-dec> <type-body> <type-body-stat> <optional-args> <optional-inherits> <optional-inherits-args>')
    
    sum, sub, mul, div, pow1, pow2, num, id, opar, cpar, ocurl, ccurl, coma, semicolon, at, function, arrow, let, in_token, asign_equal, asign, if_token, elif_token, else_token, and_token, or_token, lower, greater, lower_equal, greater_equal, equal, diferent, true, false, while_token, for_token, type_token, inherits, new = G.Terminals('+ - * / ^ ** num id ( ) { } , ; @ function => let in = := if elif else & | < > <= >= == != true false while for type inherits new')    
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
    
    ### if - else###If
    expr %= if_token + opar + boolean_expr + cpar + expr + elif_token + else_token + expr, lambda h, s: IfElseNode([s[3]] + s[6][0], [s[5]] + s[6][1] + s[8]), None, None, None, None, None, None, None, None
    
    elif_expr %= elif_token + opar + boolean_expr + cpar + expr + elif_expr, lambda h, s: ([s[3]] + s[6][0], [s[5]] + s[6][1]), None, None, None, None, None, None
    elif_expr %= G.Epsilon, lambda h, s: ([], []), None
    
    boolean_expr %= boolean_term + and_token + boolean_expr, lambda h, s: BooleanExprNode(s[1], s[3], s[2]), None, None, None
    boolean_expr %= boolean_term + or_token + boolean_expr, lambda h, s: BooleanExprNode(s[1], s[3], s[2]), None, None, None
    boolean_expr %= boolean_term, lambda h, s: s[1], None, None, None
    
    boolean_term %= expr + lower + expr, lambda h, s: BinaryOperationNode(s[1], s[3], s[2]), None, None, None
    boolean_term %= expr + greater + expr, lambda h, s: BinaryOperationNode(s[1], s[3], s[2]), None, None, None
    boolean_term %= expr + lower_equal + expr, lambda h, s: BinaryOperationNode(s[1], s[3], s[2]), None, None, None
    boolean_term %= expr + greater_equal + expr, lambda h, s: BinaryOperationNode(s[1], s[3], s[2]), None, None, None
    boolean_term %= expr + equal + expr, lambda h, s: BinaryOperationNode(s[1], s[3], s[2]), None, None, None
    boolean_term %= expr + diferent + expr, lambda h, s: BinaryOperationNode(s[1], s[3], s[2]), None, None, None
    boolean_term %= true, lambda h, s: ConstantNode(s[1]), None
    boolean_term %= false, lambda h, s: ConstantNode(s[1]), None
    boolean_term %= id, lambda h, s: VariableNode(s[1]), None
    
    
    ###loops###
    expr %= while_token + opar + boolean_expr + cpar + expr, None, None, None, None, None, None
    expr %= for_token + opar + id + in_token + expr + cpar + expr, None, None, None, None, None, None, None, None
    
    return G

