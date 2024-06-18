from  ast_nodes.hulk_ast_nodes import *
from  utils.pycompiler import Grammar

G = Grammar()

expr = G.NonTerminal('<expr>', startSymbol=True)

expr_list, stringify, term, factor, atom, func_call, arg_list, dot_notation_expr = G.NonTerminals(
    '<expr-list> <stringify> <term> <factor> <atom> <func-call> <arg-list> <dot-notation-expr>')
func_def, arg_def_list, func_body = G.NonTerminals(
    '<func-def> <arg-def-list> <func-body>')
var_def, elif_expr, boolean_expr, boolean_term = G.NonTerminals(
    '<var-def> <elif_expr> boolean-expr> <boolean-term>')
type_def, type_body, type_body_stat, optional_args, optional_inherits, optional_inherits_args = G.NonTerminals(
    '<type-def> <type-body> <type-body-stat> <optional-args> <optional-inherits> <optional-inherits-args>')

sum, sub, mul, div, pow1, pow2, num, id, opar, cpar, ocurl, ccurl, dot = G.Terminals(
    '+ - * / ^ ** num id ( ) { } .')
coma, semicolon, at, function, arrow, let, in_token, asign_equal, asign = G.Terminals(
     ', ; @ function => let in = :=')
if_token, elif_token, else_token, and_token, or_token = G.Terminals(
    'if elif else & |')
lower, greater, lower_equal, greater_equal, equal, diferent = G.Terminals(
    '< > <= >= == !=')
true, false, while_token, for_token, type_token, inherits, new = G.Terminals('true false while for type inherits new')

expr %= ocurl + expr_list + ccurl, lambda h, s: BlockExprNode(s[2]), None, None, None
expr %= expr + at + stringify, lambda h, s: BinaryOperationNode(s[1], s[3], s[2]), None, None, None
expr %= stringify, lambda h, s: s[1], None

stringify %= stringify + sum + term, lambda h, s: BinaryOperationNode(s[1], s[3], s[2]), None, None, None
stringify %= stringify + sub + term, lambda h, s: BinaryOperationNode(s[1], s[3], s[2]), None, None, None
stringify %= term, lambda h, s: s[1], None

expr_list %= expr_list + semicolon + expr, lambda h, s: s[1] + [s[3]], None, None, None
expr_list %= expr, lambda h, s: [s[1]], None

term %= term + mul + factor, lambda h, s: BinaryOperationNode(s[1], s[3], s[2]), None, None, None
term %= term + div + factor, lambda h, s: BinaryOperationNode(s[1], s[3], s[2]), None, None, None
term %= factor, lambda h, s: s[1], None

factor %= atom + pow1 + factor, lambda h, s: BinaryOperationNode(s[1], s[3], s[2]), None, None, None
factor %= atom + pow2 + factor, lambda h, s: BinaryOperationNode(s[1], s[3], s[2]), None, None, None
factor %= atom, lambda h, s: s[1], None

atom %= num, lambda h, s: ConstantNode(s[1]), None
atom %= opar + expr + cpar, lambda h, s: s[2], None, None, None

dot_notation_expr %= dot_notation_expr + dot + id, lambda h, s: DotNotationNode(s[1], VariableNode(s[3])), None, None, None
dot_notation_expr %= dot_notation_expr + dot + func_call, lambda h, s: DotNotationNode(s[1], FuncCallNode(s[3])), None, None, None
dot_notation_expr %= id, lambda h, s: VariableNode(s[1]), None
dot_notation_expr %= func_call, lambda h, s: s[1], None

func_call %= id + opar + arg_list + cpar, lambda h, s: FuncCallNode(s[1], s[3]), None, None, None, None

arg_list %= arg_list + coma + expr, lambda h, s: s[1] + [s[3]], None, None, None
arg_list %= expr, lambda h, s: [s[1]], None

###functions###

func_def %= function + id + opar + arg_def_list + cpar + func_body, lambda h , s: FuncDefNode(s[2], s[4], s[6]), None, None, None, None, None, None
arg_def_list %= arg_def_list + coma + id, lambda h , s: s[1] + [s[3]], None, None, None
arg_def_list %= id , lambda h ,s: [s[1]], None
arg_def_list %= G.Epsilon, lambda h , s: []
func_body %= arrow + expr + semicolon, lambda h ,s: s[2], None, None, None
func_body %= ocurl + expr_list + ccurl, lambda h, s: BlockExprNode(s[2]), None, None, None

###variables###

expr %= let + var_def + in_token + expr, lambda h, s: LetInNode(s[2], s[4]), None, None, None, None
expr %= id + asign + expr, lambda h, s: VarReAsignNode(s[1], s[3]), None, None, None

var_def %= var_def + coma + id + asign_equal + expr, lambda h , s: s[1] + [VarDefNode(s[3], s[5])]
var_def %= id + asign_equal + expr, lambda h , s: [VarDefNode(s[1], s[3])]

### if - else ###

expr %= if_token + opar + boolean_expr + cpar + expr + elif_token + else_token + expr, lambda h, s: IfElseNode([s[3]] + s[6][0], [s[5]] + s[6][1] + s[8]), None, None, None, None, None, None, None, None

elif_expr %= elif_token + opar + boolean_expr + cpar + expr + elif_expr, lambda h, s: ([s[3]] + s[6][0], [s[5]] + s[6][1]), None, None, None, None, None, None
elif_expr %= G.Epsilon, lambda h, s: ([], [])

boolean_expr %= boolean_expr + and_token + boolean_term, lambda h, s: BooleanExprNode(s[1], s[3], s[2]), None, None, None
boolean_expr %= boolean_expr + or_token + boolean_term, lambda h, s: BooleanExprNode(s[1], s[3], s[2]), None, None, None
boolean_expr %= boolean_term, lambda h, s: s[1], None

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

###types###

type_def %= type_token + id + optional_args +  ocurl + type_body + ccurl, None, None, None, None, None, None, None
    
optional_args %= opar + arg_def_list + cpar, None, None, None, None
optional_args %= G.Epsilon, None, None

optional_inherits %= inherits + id + optional_inherits_args, None, None, None, None
optional_inherits %= G.Epsilon, None, None

optional_inherits_args %= opar + arg_list + cpar, None, None, None, None
optional_inherits_args %= G.Epsilon, None, None

type_body %= type_body_stat + semicolon + type_body, None, None, None, None,
type_body %= type_body_stat + semicolon, None, None, None

type_body_stat %= id + asign_equal + expr, None, None, None, None
type_body_stat %= id + opar + arg_def_list + cpar + func_body, None, None, None, None, None, None

expr %= new + id + opar + arg_list + cpar, None, None, None, None, None, None