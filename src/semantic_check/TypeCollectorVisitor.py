import utils.visitor as visitor
from  ast_nodes.hulk_ast_nodes import *
from Context import Context

class TypeCollector(object):
    def __init__(self, errors=[]):
        self.context = None
        self.errors = errors
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node):
        self.context = Context()
        for definition in node.definitions:
            self.visit(definition)
        return self.context

    @visitor.when(TypeDefNode)
    def visit(self, node):
        self.context = Context()
        for definition in node.definitions:
            self.visit(definition)
        return self.context
    
    @visitor.when(ProtocolDefNode)
    def visit(self, node):
        self.context = Context()
        for definition in node.definitions:
            self.visit(definition)
        return self.context
    
    @visitor.when(FuncDefNode)
    def visit(self, node):
        self.context = Context()
        for definition in node.definitions:
            self.visit(definition)
        return self.context
    