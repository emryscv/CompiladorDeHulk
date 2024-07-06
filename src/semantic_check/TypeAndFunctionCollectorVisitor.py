import utils.visitor as visitor
from  ast_nodes.hulk_ast_nodes import *
from semantic_check.context import Context
from semantic_check.Scope import Scope
from utils.error_manager import Already_Defined

class TypeAndFunctionCollector(object):
    def __init__(self, errors=[]):
        self.context = None
        self.scope = None
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
    def visit(self, node:TypeDefNode):
        if self.context.is_type_defined(node.identifier):
            self.errors.append(Already_Defined("Type", node.identifier, node.row, node.col))
        elif self.context.is_protocol_defined(node.identifier):
            self.errors.append(Already_Defined("Protocol", node.identifier, node.row, node.col))
            
        self.context.create_type(node.identifier)
    
    @visitor.when(ProtocolDefNode)
    def visit(self, node):
        if self.context.is_type_defined(node.identifier):
            self.errors.append(Already_Defined("Type", node.identifier, node.row, node.col))
        elif self.context.is_protocol_defined(node.identifier):
            self.errors.append(Already_Defined("Protocol", node.identifier, node.row, node.col))
            
        self.context.create_protocol(node.identifier)
    
    @visitor.when(FuncDefNode)
    def visit(self, node: FuncDefNode):
        params = [(param[0], param[1].lex if param[1] else "Object") for param in node.params_list]
        return_type = node.return_type_token.lex if node.return_type_token else "Object" 
        
        if self.scope.define_function(node.identifier, params, return_type):
            self.errors.append(Already_Defined("Function", node.identifier, node.row, node.col))
