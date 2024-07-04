import utils.visitor as visitor
import math
import random
from ast_nodes.hulk_ast_nodes import *

class Interpreter:
    def __init__(self,context):
        self.context = context
        built_in_functions = {
            "print": lambda x: print(x[0]),
            "sen": lambda x: math.sin(x[0]),
            "cos": lambda x: math.cos(x[0]),
            "tan": lambda x: math.tan(x[0]),
            "sqrt": lambda x: math.sqrt(x[0]),
            "exp": lambda x: x[0]**x[1],
            "log": lambda x: math.log(x[0], x[1]),
            "rand": lambda x: random.random,
            "range": lambda x: list(range(x[0], x[1]))
        }

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        program_scope = {}

        for definition in node.definitions:
            self.visit(definition, program_scope)
        
        self.visit(node.mainExpression, program_scope)
        
    @visitor.when(DeclarationNode)
    def visit(self, node, scope):
        pass

    @visitor.when(TypeDefNode)
    def visit(self, node, scope):
        pass

    @visitor.when(ProtocolDefNode)
    def visit(self, node, scope):
        pass

    @visitor.when(FuncDecNode)
    def visit(self, node, scope):
        pass

    @visitor.when(FuncDefNode)
    def visit(self, node, scope):
        pass

    @visitor.when(ExpressionNode)
    def visit(self, node, scope):
        pass

    @visitor.when(BlockExprNode)
    def visit(self, node, scope):
        pass

    @visitor.when(LetInNode)
    def visit(self, node, scope):
        pass

    @visitor.when(VarDefNode)
    def visit(self, node, scope):
        pass

    @visitor.when(IfElseNode)
    def visit(self, node, scope):
        pass

    @visitor.when(WhileLoopNode)
    def visit(self, node, scope):
        pass

    @visitor.when(ForLoopNode)
    def visit(self, node, scope):
        pass

    @visitor.when(BinaryOperationNode)
    def visit(self, node, scope):
        pass

    @visitor.when(BooleanExprNode)
    def visit(self, node, scope):
        pass

    @visitor.when(VarReAsignNode)
    def visit(self, node, scope):
        pass

    @visitor.when(DotNotationNode)
    def visit(self, node, scope):
        pass

    @visitor.when(FuncCallNode)
    def visit(self, node, scope):
        pass

    @visitor.when(AtomicNode)
    def visit(self, node, scope):
        pass

    @visitor.when(ConstantNode)
    def visit(self, node, scope):
        pass

    @visitor.when(VariableNode)
    def visit(self, node, scope):
        pass

    @visitor.when(NewInstanceNode)
    def visit(self, node, scope):
        pass