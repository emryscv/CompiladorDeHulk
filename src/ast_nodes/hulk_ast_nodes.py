from ast_nodes.ast_base_nodes import BinaryNode, AtomicNode, Node
import utils.visitor as visitor

class ConstantNumberNode(AtomicNode):
    pass

class VariableNode(AtomicNode):
    pass

class BinaryOperationNode(BinaryNode):
    def __init__(self, left, right, operator):
        super().__init__(left, right)
        self.operator = operator

class BlockExprNode(Node):
    def __init__(self, expr_list):
        self.expr_list = expr_list

class FuncCallNode(Node):
    def __init__(self, identifier, arg_list):
        super().__init__()
        self.identifier = identifier
        self.arg_list = arg_list
        
def get_printer(AtomicNode=AtomicNode, BinaryNode=BinaryOperationNode, FuncCallNode=FuncCallNode):

    class PrintVisitor(object):
        @visitor.on('node')
        def visit(self, node, tabs):
            pass

        @visitor.when(BinaryNode)
        def visit(self, node, tabs=0):
            ans = '\t' * tabs + f'\\__<expr> {node.__class__.__name__}  {node.operator} <expr>'
            left = self.visit(node.left, tabs + 1)
            right = self.visit(node.right, tabs + 1)
            return f'{ans}\n{left}\n{right}'

        @visitor.when(AtomicNode)
        def visit(self, node, tabs=0):
                
            return '\t' * tabs + f'\\__ {node.__class__.__name__}: {node.lex}'

        
        @visitor.when(FuncCallNode)
        def visit(self, node, tabs=0):
            arg = ""
            for expr in node.arg_list:
               arg += self.visit(expr, tabs+1) + f'\n {"\t" * (tabs+1)};\n'
            return '\t' * tabs + f'\\__ {node.__class__.__name__}: {node.identifier} args: {{ \n   {arg}{"\t" * tabs}}}'

    printer = PrintVisitor()
    return (lambda ast: printer.visit(ast))