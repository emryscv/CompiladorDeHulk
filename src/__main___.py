import grammars.HULK_grammar
from ast_nodes.hulk_ast_nodes import *

printer = get_printer(AtomicNode=ConstantNode, BinaryNode=BinaryOperationNode, FuncCallNode=FuncCallNode)

print(printer(
    BinaryOperationNode(
        ConstantNode(2),
        BinaryOperationNode(
            FuncCallNode(
                "print", 
                [
                    BinaryOperationNode(
                        ConstantNode(2),
                        ConstantNode(2),
                        "/"
                    ),
                    BinaryOperationNode(
                        ConstantNode(2),
                        ConstantNode(2),
                        "/"
                    )
                ]  
                ),
                ConstantNode(3),
                "^"
            ),
            "+"
        )
    )
)

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