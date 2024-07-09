import utils.visitor as visitor
from ast_nodes.hulk_ast_nodes import *
from semantic_check.context import Context
from semantic_check.Scope import Scope
from utils.error_manager import Already_Defined
from  grammars.HULK_grammar import *

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
        
        
        self.scope.define_function("print", [("string", self.context.get_type("Object")[1])], self.context.get_type("Object")[1])
        self.scope.define_function("range", [("min", self.context.get_type("Number")[1]), ("max", self.context.get_type("Number")[1])], self.context.get_type("Range")[1])      
        self.scope.define_function("sqrt", [("value", self.context.get_type("Number")[1])], self.context.get_type("Number")[1])
        self.scope.define_function("sin", [("angle", self.context.get_type("Number")[1])], self.context.get_type("Number")[1])
        self.scope.define_function("cos", [("angle", self.context.get_type("Number")[1])], self.context.get_type("Number")[1])
        self.scope.define_function("exp", [("value", self.context.get_type("Number")[1])], self.context.get_type("Number")[1])
        self.scope.define_function("log", [("base", self.context.get_type("Number")[1]), ("value", self.context.get_type("Number")[1])], self.context.get_type("Number")[1])
        self.scope.define_function("rand", [], self.context.get_type("Number")[1])  
        
        self.scope.define_variable("PI", self.context.get_type("Number")[1])
        self.scope.define_variable("E", self.context.get_type("Number")[1])
        
        #TODO definir sin, cos, etc...
        #despues de eso comprobar los parametros en los tipos

        return self.context, self.scope

    @visitor.when(TypeDefNode)
    def visit(self, node:TypeDefNode):
        if self.context.is_type_defined(node.identifier.lex):
            self.errors.append(Already_Defined("Type", node.identifier))
        elif self.context.is_protocol_defined(node.identifier.lex):
            self.errors.append(Already_Defined("Protocol", node.identifier))
            
        self.context.create_type(node.identifier.lex)
    
    @visitor.when(ProtocolDefNode)
    def visit(self, node):
        if self.context.is_type_defined(node.identifier.lex):
            self.errors.append(Already_Defined("Type", node.identifier))
        elif self.context.is_protocol_defined(node.identifier):
            self.errors.append(Already_Defined("Protocol", node.identifier))
            
        self.context.create_protocol(node.identifier.lex)
    
    @visitor.when(FuncDefNode)
    def visit(self, node: FuncDefNode):
        params = [(param[0], param[1] if param[1] else Token("Object", id, param[0].row, param[0].column)) for param in node.params_list]
        return_type = node.return_type_token if node.return_type_token else Token("Object", id, node.identifier.row, node.identifier.column)
        
        if self.scope.define_function(node.identifier.lex, params, return_type):
            self.errors.append(Already_Defined("Function", node.identifier))
