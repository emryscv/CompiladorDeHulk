import utils.visitor as visitor
from ast_nodes.hulk_ast_nodes import *

class CodeGenerator():
    def __init__(self):
        pass

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        pass

    @visitor.when(DeclarationNode)
    def visit(self, node):
        pass

    @visitor.when(TypeDefNode)
    def visit(self, node):
        pass

    @visitor.when(ProtocolDefNode)
    def visit(self, node):
        pass

    @visitor.when(FuncDecNode)
    def visit(self, node):
        pass

    @visitor.when(FuncDefNode)
    def visit(self, node):
        pass

    @visitor.when(ExpressionNode)
    def visit(self, node):
        pass

    @visitor.when(BlockExprNode)
    def visit(self, node):
        pass

    @visitor.when(LetInNode)
    def visit(self, node):
        pass

    @visitor.when(VarDefNode)
    def visit(self, node):
        pass

    @visitor.when(IfElseNode)
    def visit(self, node):
        pass

    @visitor.when(WhileLoopNode)
    def visit(self, node):
        pass

    @visitor.when(ForLoopNode)
    def visit(self, node):
        pass

    @visitor.when(BinaryOperationNode)
    def visit(self, node):
        pass

    @visitor.when(BooleanExprNode)
    def visit(self, node):
        pass

    @visitor.when(VarReAsignNode)
    def visit(self, node):
        pass

    @visitor.when(DotNotationNode)
    def visit(self, node):
        pass

    @visitor.when(FuncCallNode)
    def visit(self, node):
        pass

    @visitor.when(AtomicNode)
    def visit(self, node):
        pass

    @visitor.when(ConstantNode)
    def visit(self, node):
        pass

    @visitor.when(VariableNode)
    def visit(self, node):
        pass

    @visitor.when(NewInstanceNode)
    def visit(self, node):
        pass