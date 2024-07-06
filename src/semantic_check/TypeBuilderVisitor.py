import utils.visitor as visitor
from  ast_nodes.hulk_ast_nodes import *
from semantic_check.context import Context
from utils.error_manager import Not_Defined, Already_Denfined_In_Type

class TypeBuilder(object):
    def __init__(self, context, errors=[]):
        self.context: Context = context
        self.current_type = None
        self.current_protocol = None
        self.errors = errors
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node):
        for definition in node.definitions:
            self.visit(definition)

    @visitor.when(TypeDefNode)
    def visit(self, node:TypeDefNode):
        self.current_type = self.context.get_type(node.identifier)
        
        if node.base_identifier:
            if self.context.is_type_defined(node.base_identifier.lex):
                parent = self.context.get_type(node.base_identifier.lex)
            else:
                parent = self.context.get_type("Object")
                self.errors.append(Not_Defined("Type", node.base_identifier.lex, node.base_identifier.row, node.base_identifier.col))
        else:
            parent = self.context.get_type("Object")
                   
        self.current_type.parent = parent
        self.current_type.params = [(param[0], param[1].lex if param[1] else "Object") for param in node.optional_params]
        
        for definition in node.body:
            self.visit(definition)
                
    @visitor.when(ProtocolDefNode)
    def visit(self, node:ProtocolDefNode):
        self.current_protocol = self.context.get_protocol(node.identifier)
        
        if node.base_identifier:            
            if self.context.is_protocol_defined(node.base_identifier.lex):
                parent = self.context.get_protocol(node.base_identifier.lex)
                self.current_protocol.parent = parent        
            else:
                self.errors.append(Not_Defined("Protocol", node.base_identifier.lex, node.base_identifier.row, node.base_identifier.col))
        
        for definition in node.body:
            self.visit(definition)
        
    @visitor.when(FuncDecNode)
    def visit(self, node: FuncDecNode):
        for param in node.params_list:
            params = (param[0], param[1].lex) 
        
        return_type = node.return_type_token.lex if node.return_type_token else "Object" 
        
        if not self.current_protocol.declare_method(node.identifier, params, return_type):
            self.errors.append(Already_Denfined_In_Type("Method", node.identifier, return_type, node.row, node.col))
            
    @visitor.when(FuncDefNode)
    def visit(self, node:FuncDefNode):
        pass
    
    @visitor.when(MethodDefNode) #TODO definir metdodos con distintos tipos de parametros
    def visit(self, node: MethodDefNode):
        params = [(param[0], param[1].lex) for param in node.params_list]
        return_type =node.return_type_token.lex if node.return_type_token else "Object" 
        
        if not self.current_type.define_method(node.identifier, params, return_type):
            self.errors.append(Already_Denfined_In_Type("Method", node.identifier, self.current_type.name, node.row, node.col))

    @visitor.when(AttributeDefNode)
    def visit(self, node:AttributeDefNode):
        if not self.current_type.define_attribute(node.identifier, node.vtype_token.lex if node.vtype_token else "Object"):
            self.errors.append(Already_Denfined_In_Type("Attribute", node.identifier, self.current_type.name, node.row, node. col))
    
        
    