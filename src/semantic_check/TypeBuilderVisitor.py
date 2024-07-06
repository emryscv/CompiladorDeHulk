import utils.visitor as visitor
from  ast_nodes.hulk_ast_nodes import *
from semantic_check.context import Context

class TypeBuilder(object):
    def __init__(self, context, errors=[]):
        self.context: Context = context
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
        message = self.context.is_type_defined(node.base_identifier.lex if node.base_identifier else "Object")
        self.current_type = self.context.get_type(node.identifier)
        
        if len(message) == 0:
            parent = self.context.get_type(node.base_identifier.lex if node.base_identifier else "Object")
            self.current_type.parent = parent
        else:
            self.errors += message
            
        self.current_type.params = [(param[0], param[1].lex if param[1] else "Object") for param in node.optional_params]
        
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
        self.errors += self.current_type.define_method(node.identifier, node.params_list, node.return_type_token.lex if node.return_type_token else "Object")

    @visitor.when(VarDefNode)
    def visit(self, node):
        self.errors += self.current_type.define_attribute(node.identifier, node.vtype_token.lex if node.vtype_token else "Object")
    
        
    