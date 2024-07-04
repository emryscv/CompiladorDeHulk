import utils.visitor as visitor
from  ast_nodes.hulk_ast_nodes import *
from Scope import Scope

class FormatVisitor(object):
    def __init__(self):
        self.errors = []
    
    @visitor.on('node')
    def visit(self, node, scope):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node, scope=None):
        scope = Scope()
        for stat in node.statements: self.visit(stat, scope)
        return self.errors
    
    @visitor.when(BinaryOperationNode)
    def visit(self, node, scope):
        return
    
    @visitor.when(AtomicNode)
    def visit(self, node, scope):
        return