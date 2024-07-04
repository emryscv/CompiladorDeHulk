import utils.visitor as visitor
from  ast_nodes.hulk_ast_nodes import *
from semantic_check.Context import Context
from semantic_check.Scope import Scope

class TypeBuilder(object):
    def __init__(self, context, errors=[]):
        self.context = context
        self.current_type = None
        self.errors = errors
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node):
        self.context = Context()
        self.scope = Scope()
        for definition in node.definitions:
            self.visit(definition)
        return self.context, self.scope

    @visitor.when(TypeDefNode)
    def visit(self, node):
        parent = self.context.get_type(node.base_identifier if node.base_identifier else "Object")
        type = self.context.get_type(node.identifier)
        type.parent = parent
        
    @visitor.when(ProtocolDefNode)
    def visit(self, node):
        pass
    
    @visitor.when(FuncDefNode)
    def visit(self, node):
        pass
    
    @visitor.when(ProtocolDefNode)
    def visit(self, node):
        pass
    