import utils.visitor as visitor
from  ast_nodes.hulk_ast_nodes import *
from semantic_check.context import Context
from semantic_check.Scope import Scope
from utils.error_manager import Not_Defined, Already_Defined_In,Forbiden_Extends, Forbiden_Inheritance, Already_Defined
from grammars.HULK_grammar import *

class TypeAndFunctionBuilder(object):
    def __init__(self, context, errors = []):
        self.context: Context = context
        self.current_type = None
        self.current_protocol = None
        self.errors = errors
    
    @visitor.on('node')
    def visit(self, node, scope):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node, scope):
        for definition in node.definitions:
            self.visit(definition, scope)
            
    @visitor.when(TypeDefNode)
    def visit(self, node:TypeDefNode, scope):
        self.current_type = self.context.get_type(node.identifier.lex)[1]
        
        if node.base_identifier:
            if node.base_identifier.lex in ["Number", "String", "Boolean", "Object"]:
                self.errors.append(Forbiden_Inheritance(node.base_identifier))
                
            success, parent = self.context.get_type(node.base_identifier.lex)
            if not success:
                self.errors.append(Not_Defined("Type", node.base_identifier))
                if self.context.is_protocol_defined(node.base_identifier.lex):
                    self.errors.append(Forbiden_Inheritance(node.base_identifier))
        else:
            _, parent = self.context.get_type("Object")
            
        params = []
        
        for param in self.current_type.params:
            param_type = param[1] if not param[1] else Token("Object", id, param[0].row, param[0].column)
            
            sucess, type = self.context.get(param_type.lex)
            if not sucess:
                self.errors.append(Not_Defined("Type", param_type))      
            params.append(param[0], type)
        
        self.current_type.params = params
        self.current_type.parent = parent
            
        for definition in node.body:
            self.visit(definition)
                
    @visitor.when(ProtocolDefNode)
    def visit(self, node:ProtocolDefNode, scope):
        self.current_protocol = self.context.get_protocol(node.identifier.lex)[1]
        
        if node.base_identifier:            
            sucess, parent = self.context.get_protocol(node.base_identifier.lex)
            if sucess:
                self.current_protocol.parent = parent        
            else:
                self.errors.append(Not_Defined("Protocol", node.base_identifier))
                if self.context.is_type_defined(node.base_identifier.lex):
                    self.errors.append(Forbiden_Extends(node.base_identifier))
        
        for definition in node.body:
            self.visit(definition)
        
    @visitor.when(FuncDecNode)
    def visit(self, node: FuncDecNode):
        #siempre hay tipo por como esta definida la gramatica
        sucess, return_type = self.context.get(node.return_type_token.lex)
        if not sucess:
            self.errors.append(Not_Defined("Type", node.return_type_token))
        
        params_name = {"*"} #python things
        params = []
        
        for param in node.params_list:
            #siempre hay tipo por como esta definida la gramatica
            sucess, type = self.context.get(param[1].lex) 
            if not sucess:
                self.errors.append(Not_Defined("Type", param[1]))
            if param[0].lex in params_name:
                self.errors.append(Already_Defined("Parameter", param[0]))
            else:   
                params_name.add(param[0].lex) 
            params.append((param[0], type))
        
        if not self.current_protocol.declare_method(node.identifier.lex, params, return_type):
            self.errors.append(Already_Defined_In("Method", node.identifier, self.current_protocol.name))
            
    @visitor.when(FuncDefNode)
    def visit(self, node:FuncDefNode, scope: Scope):
        function = scope.get_function(node.identifier.lex)
        
        #siempre hay tipo por el recorrido de type collection
        sucess, function.return_type = self.context.get(function.return_type.lex)
        if not sucess:
            #si falla es porq habia un token porq sin oes object
            self.errors.append(Not_Defined("Type", node.return_type_token))
        
        params = []
        
        for param in function.params:
            #siempre hay tipo por el recorrido de type collection
            sucess, type = self.context.get(param[1].lex) 
            if not sucess:
                self.errors.append(Not_Defined("Type", param[1]))
            params.append((param[0], type))
        
        function.params = params 
        
    @visitor.when(MethodDefNode) #TODO definir metdodos con distintos tipos de parametros
    def visit(self, node: MethodDefNode):
        #Hay q comprobar que halla token tipo
        sucess, return_type = self.context.get(node.return_type_token.lex if node.return_type_token else "Object")
        if not sucess:
            self.errors.append(Not_Defined("Type", node.return_type_token))

        params = []
        
        for param in node.params_list:
            #Hay q comprobar que halla token tipo
            sucess, type = self.context.get(param[1].lex if param[1] else "Object") 
            if not sucess:
                self.errors.append(Not_Defined("Type", param[1]))
            params.append((param[0], type))
        
        if not self.current_type.define_method(node.identifier.lex, params, return_type):
            self.errors.append(Already_Defined_In("Method", node.identifier, self.current_type.name))

    @visitor.when(AttributeDefNode)
    def visit(self, node:AttributeDefNode):
        #Hay q comprobar que halla token tipo
        sucess, vtype = self.context.get(node.vtype_token.lex if node.vtype_token else "Object")
        if not sucess:
            self.errors.append(Not_Defined("Type", node.vtype_token))
        
        if not self.current_type.define_attribute(node.identifier.lex, vtype):
            self.errors.append(Already_Defined_In("Attribute", node.identifier, self.current_type.name))
    
        
    