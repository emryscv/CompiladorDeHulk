import utils.visitor as visitor
from  ast_nodes.hulk_ast_nodes import *
from semantic_check.context import Context
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
        for definition in node.definitions:
            self.visit(definition)

    @visitor.when(TypeDefNode)
    def visit(self, node):
        parent = self.context.get_type(node.base_identifier if node.base_identifier else "Object")
        self.current_type = self.context.get_type(node.identifier)
        self.current_type.parent = parent
        
        for definition in node.body:
            self.visit(definition)
                
    @visitor.when(ProtocolDefNode)
    def visit(self, node):
        pass
    
    @visitor.when(FuncDefNode)
    def visit(self, node):
        pass
    
    @visitor.when(MethodDefNode)
    def visit(self, node):
        self.errors += self.current_type.define_method(node.identifier, node.params_list, node.return_type)
     
    @visitor.when(VarDefNode)
    def visit(self, node):
        self.errors += self.current_type.define_attribute(node.identifier, node.type)
    
        
    