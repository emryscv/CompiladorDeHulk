from src.ast_nodes.ast_base_nodes import Node, UnaryNode, BinaryNode


class EpsilonNode(Node):
    pass

class SymbolNode(UnaryNode):
    pass

class ClousureNode(UnaryNode):
    pass

class UnionNode(BinaryNode):
    pass

class ConcatNode(BinaryNode):
    pass
    