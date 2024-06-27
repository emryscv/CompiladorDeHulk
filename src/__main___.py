from grammars.HULK_grammar import *
from ast_nodes.hulk_ast_nodes import *
from parser.LR1Parser import LR1Parser
from parser.SRParser import ShiftReduceParser

parser = LR1Parser(G, verbose=True)

#derivation = parser([num, mul, num, equal, num, mul, num, G.EOF])
# #print(derivation)
derivation = parser([let, id, asign_equal, num, in_token, if_token, opar, id, equal, num, cpar, id, dot, id, opar, cpar, else_token, id, G.EOF])

# derivation = parser([opar, let, id, asign_equal, num, in_token, id, cpar, equal, let, id, asign_equal, num, in_token, id, G.EOF])

for prod in derivation:
    print(prod)
# printer = get_printer(AtomicNode=ConstantNode, BinaryNode=BinaryOperationNode, FuncCallNode=FuncCallNode)
#
# print(printer(
#     BinaryOperationNode(
#         ConstantNode(2),
#         BinaryOperationNode(
#             FuncCallNode(
#                 "print",
#                 [
#                     BinaryOperationNode(
#                         ConstantNode(2),
#                         ConstantNode(2),
#                         "/"
#                     ),
#                     BinaryOperationNode(
#                         ConstantNode(2),
#                         ConstantNode(2),
#                         "/"
#                     )
#                 ]
#                 ),
#                 ConstantNode(3),
#                 "^"
#             ),
#             "+"
#         )
#     )
# )

# def tokenize_text(text):
#     fixed_tokens = { lex: Token(lex, G[lex]) for lex in '+ - * / ^ ** num id ( ) { } , ; @'.split() }
#     tokens = []
#     for item in text.split():
#         try:
#             float(item)
#             token = Token(item, G['num'])
#         except ValueError:
#             try:
#                 token = fixed_tokens[item]
#             except:
#                 token = UnknownToken(item)
#         tokens.append(token)
#     eof = Token('$', G.EOF)
#     tokens.append(eof)
#     return tokens
#
# G = grammars.HULK_grammar.get_hulk_grammar()
# firsts = compute_firsts(G)
# follows = compute_follows(G, firsts)
#
# M = build_parsing_table(G, firsts, follows)
#
# parser = metodo_predictivo_no_recursivo(G, M)
#
# tokens = tokenize_text("4 ^ 3 ^ 2")
#
# print(tokens)
# print(parser(tokens))