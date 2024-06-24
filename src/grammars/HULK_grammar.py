from  ast_nodes.hulk_ast_nodes import *
from  utils.pycompiler import Grammar

G = Grammar()

program = G.NonTerminal('<program>', startSymbol=True)

expr, expr_list, stringify, term, factor, atom, func_call, arg_list, dot_notation_expr = G.NonTerminals(
    '<expr> <expr-list> <stringify> <term> <factor> <atom> <func-call> <arg-list> <dot-notation-expr>')
asign_simple, func_def, arg_def_list, func_body = G.NonTerminals(
    '<asign-simple> <func-def> <arg-def-list> <func-body>')
var_def, elif_expr, boolean_expr, boolean_term = G.NonTerminals(
    '<var-def> <elif_expr> boolean-expr> <boolean-term>')
type_def, type_body, type_body_stat, optional_args, optional_inherits, optional_inherits_args, let_in = G.NonTerminals(
    '<type-def> <type-body> <type-body-stat> <optional-args> <optional-inherits> <optional-inherits-args> <let-in>')

sum, sub, mul, div, pow1, pow2, num, id, opar, cpar, ocurl, ccurl, dot = G.Terminals(
    '+ - * / ^ ** num id ( ) { } .')
coma, semicolon, at, function, arrow, let, in_token, asign_equal, asign = G.Terminals(
     ', ; @ function => let in = :=')
if_token, elif_token, else_token, and_token, or_token = G.Terminals(
    'if elif else & |')
lower, greater, lower_equal, greater_equal, equal, diferent = G.Terminals(
    '< > <= >= == !=')
true, false, while_token, for_token, type_token, inherits, new = G.Terminals(
    'true false while for type inherits new')

program %= expr, None, None
program %= let_in, None, None
program %= asign_simple, None, None

expr %= ocurl + expr_list + ccurl, lambda h, s: BlockExprNode(s[2])
expr %= expr + stringify, lambda h, s: BinaryOperationNode(s[1], s[3], s[2])
expr %= stringify, lambda h, s: s[1]

stringify %= stringify + sum + term, lambda h, s: BinaryOperationNode(s[1], s[3], s[2])
stringify %= stringify + sub + term, lambda h, s: BinaryOperationNode(s[1], s[3], s[2])
stringify %= term, lambda h, s: s[1]

expr_list %= expr_list + semicolon + expr, lambda h, s: s[1] + [s[3]]
expr_list %= expr, lambda h, s: [s[1]]

term %= term + mul + factor, lambda h, s: BinaryOperationNode(s[1], s[3], s[2])
term %= term + div + factor, lambda h, s: BinaryOperationNode(s[1], s[3], s[2])
term %= factor, lambda h, s: s[1]

factor %= atom + pow1 + factor, lambda h, s: BinaryOperationNode(s[1], s[3], s[2])
factor %= atom + pow2 + factor, lambda h, s: BinaryOperationNode(s[1], s[3], s[2])
factor %= atom, lambda h, s: s[1]

atom %= num, lambda h, s: ConstantNode(s[1])
atom %= opar + expr + cpar, lambda h, s: s[2]

dot_notation_expr %= dot_notation_expr + dot + id, lambda h, s: DotNotationNode(s[1], VariableNode(s[3]))
dot_notation_expr %= dot_notation_expr + dot + func_call, lambda h, s: DotNotationNode(s[1], FuncCallNode(s[3]))
dot_notation_expr %= id, lambda h, s: VariableNode(s[1])
dot_notation_expr %= func_call, lambda h, s: s[1]

func_call %= id + opar + arg_list + cpar, lambda h, s: FuncCallNode(s[1], s[3])

arg_list %= arg_list + coma + expr, lambda h, s: s[1] + [s[3]]
arg_list %= expr, lambda h, s: [s[1]]

###functions###

func_def %= function + id + opar + arg_def_list + cpar + func_body, lambda h , s: FuncDefNode(s[2], s[4], s[6])
arg_def_list %= arg_def_list + coma + id, lambda h , s: s[1] + [s[3]]
arg_def_list %= id , lambda h ,s: [s[1]]
arg_def_list %= G.Epsilon, lambda h , s: []
func_body %= arrow + expr + semicolon, lambda h ,s: s[2]
func_body %= ocurl + expr_list + ccurl, lambda h, s: BlockExprNode(s[2])

###variables###

let_in %= let + var_def + in_token + expr, lambda h, s: LetInNode(s[2], s[4])
asign_simple %= id + asign + expr, lambda h, s: VarReAsignNode(s[1], s[3])

var_def %= var_def + coma + id + asign_equal + expr, lambda h , s: s[1] + [VarDefNode(s[3], s[5])]
var_def %= id + asign_equal + expr, lambda h , s: [VarDefNode(s[1], s[3])]

### if - else ###

# expr %= if_token + opar + boolean_expr + cpar + expr + elif_expr + else_token + expr, lambda h, s: IfElseNode([s[3]] + s[6][0], [s[5]] + s[6][1] + s[8])

# elif_expr %= elif_expr + elif_token + opar + boolean_expr + cpar + expr, lambda h, s: (s[6][0] + [s[3]], s[6][1] + [s[5]])
# elif_expr %= G.Epsilon, lambda h, s: ([], [])

# boolean_expr %= boolean_expr + and_token + boolean_term, lambda h, s: BooleanExprNode(s[1], s[3], s[2])
# boolean_expr %= boolean_expr + or_token + boolean_term, lambda h, s: BooleanExprNode(s[1], s[3], s[2])
# boolean_expr %= boolean_term, lambda h, s: s[1]

# boolean_term %= expr + lower + expr, lambda h, s: BinaryOperationNode(s[1], s[3], s[2])
# boolean_term %= expr + greater + expr, lambda h, s: BinaryOperationNode(s[1], s[3], s[2])
# boolean_term %= expr + lower_equal + expr, lambda h, s: BinaryOperationNode(s[1], s[3], s[2])
# boolean_term %= expr + greater_equal + expr, lambda h, s: BinaryOperationNode(s[1], s[3], s[2])
# boolean_term %= expr + equal + expr, lambda h, s: BinaryOperationNode(s[1], s[3], s[2])
# boolean_term %= expr + diferent + expr, lambda h, s: BinaryOperationNode(s[1], s[3], s[2])
# boolean_term %= true, lambda h, s: ConstantNode(s[1])
# boolean_term %= false, lambda h, s: ConstantNode(s[1])
# boolean_term %= id, lambda h, s: VariableNode(s[1])

# ###loops###

# expr %= while_token + opar + boolean_expr + cpar + expr
# expr %= for_token + opar + id + in_token + expr + cpar + expr

# ###types###

# type_def %= type_token + id + optional_args +  ocurl + type_body + ccurl
    
# optional_args %= opar + arg_def_list + cpar
# optional_args %= G.Epsilon

# optional_inherits %= inherits + id + optional_inherits_args
# optional_inherits %= G.Epsilon

# optional_inherits_args %= opar + arg_list + cpar
# optional_inherits_args %= G.Epsilon

# type_body %= type_body_stat + semicolon + type_body
# type_body %= type_body_stat + semicolon

# type_body_stat %= id + asign_equal + expr
# type_body_stat %= id + opar + arg_def_list + cpar + func_body

# expr %= new + id + opar + arg_list + cpar