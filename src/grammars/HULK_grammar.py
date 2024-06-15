from  ast_nodes.hulk_ast_nodes import *
from  utils.pycompiler import Grammar

G = Grammar()

program = G.NonTerminal('<program>', startSymbol=True)

definition_list, definition, arithmetic_expr, expr, expr_or_block, expr_list, stringify, term, factor, atom, func_call, arguments, arg_list, dot_notation_expr = G.NonTerminals(
    '<definition-list> <definition> <arithmetic-expr> <expr> <expr-or-block> <expr-list> <stringify> <term> <factor> <atom> <func-call> <arguments> <arg-list> <dot-notation-expr>')
asign_simple, func_def, arg_def, arg_def_list, func_body = G.NonTerminals(
    '<asign-simple> <func-def> <arg_def? <arg-def-list> <func-body>')
var_def, elif_expr, boolean_expr, boolean_term = G.NonTerminals(
    '<var-def> <elif_expr> boolean-expr> <boolean-term>')
type_def, type_body, type_body_stat, optional_args, optional_inherits, optional_inherits_args, let_in, type_annotation = G.NonTerminals(
    '<type-def> <type-body> <type-body-stat> <optional-args> <optional-inherits> <optional-inherits-args> <let-in> <type-annotation> <protocol-def> <protocol-body> <arg_def_list_protocol>')

protocol_def, protocol_body, arg_def_list_protocol = G.NonTerminals('<protocol-def> <protocol-body> <arg_def_list_protocol>') 

sum, sub, mul, div, pow1, pow2, num, id, opar, cpar, ocurl, ccurl, dot = G.Terminals(
    '+ - * / ^ ** num id ( ) { } .')
coma, semicolon, at, double_at, function, arrow, let, in_token, asign_equal, asign, colon = G.Terminals(
     ', ; @ @@ function => let in = := :')
if_token, elif_token, else_token, and_token, or_token = G.Terminals(
    'if elif else & |')
lower, greater, lower_equal, greater_equal, equal, diferent = G.Terminals(
    '< > <= >= == !=')
true, false, while_token, for_token, type_token, inherits, new, protocol = G.Terminals(
    'true false while for type inherits new protocol')
                          
program %= definition_list + expr + semicolon, lambda h, s: ProgramNode(s[1], s[2])
definition_list %= definition_list + definition, lambda h, s: s[1] + [s[2]]
definition_list %= G.Epsilon, lambda h, s: []

definition %= type_def, lambda h, s: s[1]
definition %= func_def, lambda h, s: s[1]
definition %= protocol_def, lambda h, s: s[1]

expr_or_block %= ocurl + expr_list + ccurl, lambda h, s: BlockExprNode(s[2])
expr_or_block %= expr, lambda h, s: s[1]
                                     
expr %= let_in, lambda h, s: s[1]
expr %= asign_simple, lambda h, s: s[1]

expr_list %= expr_list + expr_or_block + semicolon, lambda h, s: s[1] + [s[2]]
expr_list %= expr_or_block + semicolon, lambda h, s: [s[1]]

arithmetic_expr %= arithmetic_expr + at + stringify, lambda h, s: BinaryOperationNode(s[1], s[3], s[2])
arithmetic_expr %= arithmetic_expr + double_at + stringify, lambda h, s: BinaryOperationNode(s[1], s[3], s[2])
arithmetic_expr %= stringify, lambda h, s: s[1]

stringify %= stringify + sum + term, lambda h, s: BinaryOperationNode(s[1], s[3], s[2])
stringify %= stringify + sub + term, lambda h, s: BinaryOperationNode(s[1], s[3], s[2])
stringify %= term, lambda h, s: s[1]

term %= term + mul + factor, lambda h, s: BinaryOperationNode(s[1], s[3], s[2])
term %= term + div + factor, lambda h, s: BinaryOperationNode(s[1], s[3], s[2])
term %= factor, lambda h, s: s[1]

factor %= atom + pow1 + factor, lambda h, s: BinaryOperationNode(s[1], s[3], s[2])
factor %= atom + pow2 + factor, lambda h, s: BinaryOperationNode(s[1], s[3], s[2])
factor %= atom, lambda h, s: s[1]

atom %= num, lambda h, s: ConstantNode(s[1]) #TODO cambiar num por constante
atom %= opar + expr_or_block + cpar, lambda h, s: s[2]
atom %= dot_notation_expr,  lambda h, s: s[1]

dot_notation_expr %= dot_notation_expr + dot + id, lambda h, s: DotNotationNode(s[1], VariableNode(s[3]))
dot_notation_expr %= dot_notation_expr + dot + func_call, lambda h, s: DotNotationNode(s[1], FuncCallNode(s[3]))
dot_notation_expr %= id, lambda h, s: VariableNode(s[1])
dot_notation_expr %= func_call, lambda h, s: s[1]

func_call %= id + opar + arguments + cpar, lambda h, s: FuncCallNode(s[1], s[3])

arguments %= G.Epsilon, lambda h, s: []
arguments %= arg_list,  lambda h, s: s[1]

arg_list %= arg_list + coma + expr_or_block, lambda h, s: s[1] + [s[3]]
arg_list %= expr_or_block, lambda h, s: [s[1]]

###functions###

func_def %= function + id + opar + arg_def_list + cpar + type_annotation + func_body, lambda h , s: FuncDefNode(s[2], s[4], s[6], s[7])

arg_def %= arg_def_list, lambda h , s: s[1]
arg_def %= G.Epsilon, lambda h , s: []

arg_def_list %= arg_def_list + coma + id + type_annotation, lambda h , s: s[1] + [(s[3], s[4])]
arg_def_list %= id + type_annotation , lambda h ,s: [(s[1], s[2])]

func_body %= arrow + expr + semicolon, lambda h ,s: s[2]
func_body %= ocurl + expr_list + ccurl, lambda h, s: BlockExprNode(s[2])

###variables###

let_in %= let + var_def + in_token + expr_or_block, lambda h, s: LetInNode(s[2], s[4])
asign_simple %= id + asign + expr_or_block, lambda h, s: VarReAsignNode(s[1], s[3])

var_def %= var_def + coma + id + type_annotation + asign_equal + expr_or_block, lambda h , s: s[1] + [VarDefNode(s[3], s[4], s[6])]
var_def %= id + type_annotation + asign_equal + expr_or_block, lambda h , s: [VarDefNode(s[1], s[2], s[4])]

### if - else ###

expr %= if_token + opar + boolean_expr + cpar + expr_or_block + elif_expr + else_token + expr_or_block, lambda h, s: IfElseNode([s[3]] + s[6][0], [s[5]] + s[6][1] + s[8])

elif_expr %= elif_expr + elif_token + opar + boolean_expr + cpar + expr_or_block, lambda h, s: (s[6][0] + [s[3]], s[6][1] + [s[5]])
elif_expr %= G.Epsilon, lambda h, s: ([], [])

expr %= boolean_expr, lambda h, s: s[1]

boolean_expr %= boolean_expr + and_token + boolean_term, lambda h, s: BooleanExprNode(s[1], s[3], s[2])
boolean_expr %= boolean_expr + or_token + boolean_term, lambda h, s: BooleanExprNode(s[1], s[3], s[2])
boolean_expr %= boolean_term, lambda h, s: s[1]

boolean_term %= boolean_term + lower + arithmetic_expr, lambda h, s: BinaryOperationNode(s[1], s[3], s[2])
boolean_term %= boolean_term + greater + arithmetic_expr, lambda h, s: BinaryOperationNode(s[1], s[3], s[2])
boolean_term %= boolean_term + lower_equal + arithmetic_expr, lambda h, s: BinaryOperationNode(s[1], s[3], s[2])
boolean_term %= boolean_term + greater_equal + arithmetic_expr, lambda h, s: BinaryOperationNode(s[1], s[3], s[2])
boolean_term %= boolean_term + equal + arithmetic_expr, lambda h, s: BinaryOperationNode(s[1], s[3], s[2])
boolean_term %= boolean_term + diferent + arithmetic_expr, lambda h, s: BinaryOperationNode(s[1], s[3], s[2])
boolean_term %= true, lambda h, s: ConstantNode(s[1])
boolean_term %= false, lambda h, s: ConstantNode(s[1])
boolean_term %= arithmetic_expr, lambda h, s: s[1]

###loops###

expr %= while_token + opar + boolean_expr + cpar + expr_or_block,  lambda h, s: WhileLoop(s[3], s[5])
expr %= for_token + opar + id + type_annotation + in_token + expr_or_block + cpar + expr_or_block, None

###types###

type_def %= type_token + id + optional_args + optional_inherits + ocurl + type_body + ccurl, lambda h, s: TypeDefNode(s[2], s[3], s[4][0], s[4][1], s[6])
    
optional_args %= opar + arg_def_list + cpar, lambda h, s: s[2]
optional_args %= G.Epsilon, lambda h, s: []

optional_inherits %= inherits + id + optional_inherits_args, lambda h, s: (s[2], s[3])
optional_inherits %= G.Epsilon, lambda h, s: ("", [])

optional_inherits_args %= opar + arg_list + cpar, lambda h, s: s[2]
optional_inherits_args %= G.Epsilon, lambda h, s: []

type_body %= type_body + type_body_stat + semicolon, lambda h , s: s[1] + [s[3]]
type_body %= type_body_stat + semicolon, lambda h , s: [s[1]]

type_body_stat %= id + type_annotation + asign_equal + expr_or_block, lambda h, s: VarDefNode(s[1], s[2], s[4]) 
type_body_stat %= id + opar + arg_def_list + cpar + type_annotation + func_body, lambda h, s: FuncDefNode(s[1], s[3], s[5], s[6])

expr %= new + id + opar + arg_list + cpar, lambda h, s: NewInstanceNode(s[2], s[4])

type_annotation %= colon + id, lambda h, s: s[2]
type_annotation %= G.Epsilon, lambda h, s: None # esto hace falta?

###protocols###

protocol_def %= protocol + id + ocurl + protocol_body + ccurl, lambda h, s: ProtocolDefNode(s[2], s[4])

protocol_body %= protocol_body + id + opar + arg_def_list_protocol + cpar + colon + id + semicolon, lambda h, s: s[1] + [FuncDecNode(s[2], s[4], s[6])]
protocol_body %= G.Epsilon, lambda h, s: []

arg_def_list_protocol %= arg_def_list_protocol + coma + id + colon + id, lambda h , s: s[1] + [(s[3], s[5])]
arg_def_list_protocol %= id + colon + id, lambda h , s: [(s[1], s[3])]