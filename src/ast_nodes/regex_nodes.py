from src.ast_nodes.ast_base_nodes import Node, UnaryNode, BinaryNode, AtomicNode


class EpsilonNode(Node):
    pass


class SymbolNode(AtomicNode):
    pass


class ClosureNode(UnaryNode):
    pass


class UnionNode(BinaryNode):
    pass


class ConcatNode(BinaryNode):
    pass
