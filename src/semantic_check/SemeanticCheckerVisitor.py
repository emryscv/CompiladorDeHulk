import utils.visitor as visitor
from  ast_nodes.hulk_ast_nodes import *
from utils.error_manager import Not_Defined, Invalid_Argument_Type, Invalid_Initialize_type, Invalid_Operation, Self_Not_Target, Boolean_Expected, Invalid_Arg_Count, Already_Defined, Already_Defined_In, Not_Defined_In
from semantic_check.Scope import Scope
from semantic_check.context import Context
from semantic_check.utils.Type import Type
from semantic_check.utils.Protocol import Protocol

class SemeanticChecker(object):
    def __init__(self, errors, context):
        self.errors = errors
        self.context: Context = context
        self.current_type: Type = None
        
    @visitor.on('node')
    def visit(self, node, scope: Scope):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node, scope: Scope):
        for definition in node.definitions: 
            self.visit(definition, scope.create_child_scope())                        
            self.current_type = None
            self.current_protocol = None
            
        self.visit(node.mainExpression, scope)

    @visitor.when(TypeDefNode)
    def visit(self, node: TypeDefNode, scope: Scope):#TODO hecarle un ojo al parent
        _, self.current_type = self.context.get_type(node.identifier.lex)


        print("params", self.current_type.params)
        params = []        
        for param in self.current_type.params:   
            if not scope.define_variable(param[0].lex, param[1]):
                self.errors.append(Already_Defined("Parameter", param[0]))
            params.append((param[0].lex, param[1]))
        
        self.current_type.params = params
        
        
        print("chequeo params", self.current_type.params)
        if len(self.current_type.params) > 0:
            print("chequeo params")
            params = self.current_type.parent.get_params()
            if len(params) != len(node.optional_base_args):
                self.errors.append(Invalid_Arg_Count(node.base_identifier, len(params), len(node.optional_base_args)))
                print("chequeo params fail")
            else:
                print("chequeo params success")
                for i, arg in enumerate(node.optional_base_args):
                    arg_type = self.visit(arg, scope)
                    print("arg", arg_type, "param", params[i][1])
                    if not arg_type.match(params[i][1]):
                        self.errors.append(Invalid_Argument_Type(i, node.identifier.lex, params[i][1].name, arg_type.name, node.base_identifier.row, node.base_identifier.column))
        
        #TODO revisar
        #Los metodos no estan en el scope son de self    
        #for method in self.current_type.methods:
        #    scope.define_function(method.name, method.params, method.return_type)
        
        scope.define_variable("self", self.current_type.name)
        
        for definition in node.body:
            self.visit(definition, scope)
    
    @visitor.when(ProtocolDefNode)
    def visit(self, node:ProtocolDefNode, scope: Scope):
        pass
            
    @visitor.when(FuncDefNode)
    def visit(self, node:FuncDefNode, scope: Scope):
        function = scope.get_function(node.identifier.lex)
        
        params = []
        for param in function.params:
            if not scope.define_variable(param[0].lex, param[1]):
                self.errors.append(Already_Defined_In("Parameter", param[0], node.identifier.lex))        
            params.append((param[0].lex, param[1]))
        
        function.params = params
        
        self.visit(node.body, scope)
    
    @visitor.when(MethodDefNode)
    def visit(self, node:MethodDefNode, scope: Scope):
        _, _, _, function = self.current_type.get_method(node.identifier.lex, len(node.params_list), self.context.get(node.return_type_token.lex if node.return_type_token else "Object")[1])
       
        params = []
        for param in function.params:
            if not scope.define_variable(param[0].lex, param[1]):
                self.errors.append(Already_Defined_In("Parameter", param[0], node.identifier.lex))        
            params.append((param[0].lex, param[1]))
        
        function.params = params      
        
        name_match, params_match, return_match, _ = self.current_type.get_method(function.name, len(function.params), function.return_type, False)
        if (name_match, params_match, return_match) == (True, True, True):
            scope.define_function("base", function.params, function.return_type)
            
        self.visit(node.body, scope)
    
    @visitor.when(BlockExprNode)
    def visit(self, node, scope):
        for i, expr in enumerate(node.expr_list):
            expr_type = self.visit(expr, scope)

            if i == len(node.expr_list) - 1:
                return expr_type
            
    # @visitor.when(LetInNode)
    # def visit(self, node, scope):
    #     inner_scope = scope.create_child_scope()
        
    #     for var in node.var_list: 
    #         self.visit(var, inner_scope)
            
    #     return self.visit(node.body, inner_scope)
    
    # @visitor.when(VarDefNode)
    # def visit(self, node:VarDefNode, scope:Scope):
    #     scope.define_variable(node.identifier, node.vtype_token.lex if node.vtype_token else "Object", check=False)

    #     expr_type = self.context.get_type(self.visit(node.expr, scope))

    #     if node.identifier == "self":
    #         scope.is_self_asignable = True
        
    #     if node.vtype_token:
    #         if not node.vtype_token.lex in self.context.types: #TODO arreglar esta vaina
    #             self.errors.append(Not_Defined("Type", node.vtype_token))
    #             return "Object"
    #         else: 
    #             if not expr_type.conformed_by(node.vtype_token.lex):
    #                 if self.context.is_protocol_defined(node.vtype_token.lex):
    #                     protocol = self.context.get_protocol(node.vtype_token.lex)
    #                     if not expr_type.implements(protocol):
    #                         self.errors.append(Invalid_Initialize_type(node.identifier, node.vtype_token.lex, expr_type.name, node.expr.row, node.expr.col))
    #                 else:
    #                     self.errors.append(Invalid_Initialize_type(node.identifier, node.vtype_token.lex, expr_type.name, node.expr.row, node.expr.col))
    #             return node.vtype_token.lex
    #     else:
    #         scope.get_variable(node.identifier).vtype = expr_type.name
    #         return expr_type.name
    
    # @visitor.when(AttributeDefNode)
    # def visit(self, node:VarDefNode, scope:Scope):    
    #     expr_type = self.context.get_type(self.visit(node.expr, scope))

    #     if node.identifier == "self":
    #         self.errors.append(Self_Not_Target(node.row, node.col))
        
    #     if node.vtype_token:
    #          if not node.vtype_token.lex in self.context.types: #TODO arreglar esta vaina
    #              self.errors.append(Not_Defined("Type", node.vtype_token))
    #              return "Object"
    #          else: 
    #              if not expr_type.conformed_by(node.vtype_token.lex):
    #                  if self.context.is_protocol_defined(node.vtype_token.lex):
    #                      protocol = self.context.get_protocol(node.vtype_token.lex)
    #                      if not expr_type.implements(protocol):
    #                         self.errors.append(Invalid_Initialize_type(node.identifier, node.vtype_token.lex, expr_type.name, node.expr.row, node.expr.col))            
    #                  else:
    #                      self.errors.append(Invalid_Initialize_type(node.identifier, node.vtype_token.lex, expr_type.name, node.expr.row, node.expr.col))
    #              return node.vtype_token.lex
    #     else:
    #         for attribute in self.current_type.attributes:
    #             if attribute.name == node.identifier:
    #                 attribute.vtype = expr_type.name
                    
    #         return expr_type.name
            
    # @visitor.when(IfElseNode)
    # def visit(self, node, scope):
    #     for expr in node.boolExpr_List:
    #         expr_type = self.visit(expr, scope)
    #         if expr_type != "Boolean":
    #             self.errors.append(Boolean_Expected(expr_type, node.row, node.col))

    #     #TODO LCA d estos panas
    #     for expr in node.body_List:
    #         self.visit(expr, scope)
        
    # @visitor.when(WhileLoopNode)
    # def visit(self, node, scope):
    #     condition_type = self.visit(node.condition, scope)
    #     if condition_type != "Boolean":
    #         self.errors.append(Boolean_Expected(condition_type, node.condition.row, node.condition.col))

    #     return self.visit(node.body, scope) #TODO esta vaina tiene q retornar lo de la ultima iteracion o None
    
    @visitor.when(BinaryOperationNode)
    def visit(self, node:BinaryOperationNode, scope):
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)

        if node.operator.lex in ['+', '-', '*', '/', '^', '**']:
            if not (left_type.name == "Number" and right_type.name == "Number"):
                self.errors.append(Invalid_Operation(node.operator, left_type.name, right_type.name))
            return self.context.get_type("Number")[1]
        
        elif node.operator.lex in ['@', '@@']:
            if not (left_type.name in ["Number", "String", "Boolean"] and right_type.name  in ["Number", "String", "Boolean"]):
                self.errors.append(Invalid_Operation(node.operator, left_type.name, right_type.name))
            return self.context.get_type("String")[1]
    
    @visitor.when(BooleanExprNode)
    def visit(self, node:BooleanExprNode, scope):
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)
       
        if node.operator.lex in ['<', '>', '<=', '>=', '==', '!='] and not (left_type.name == "Number" and right_type.name == "Number"):
                self.errors.append(Invalid_Operation(node.operator, left_type.name, right_type.name))
        elif node.operator.lex in ['&', '|'] and not (left_type.name == "Boolean" and right_type.name == "Boolean"):
                self.errors.append(Invalid_Operation(node.operator, left_type.name, right_type.name))
    
        return self.context.get_type("Boolean")
    
    # @visitor.when(VarReAsignNode)
    # def visit(self, node, scope):
    #     message = [] #TODO 
        
    #     if not self.is_self_asignable and node.identifier == 'self':
    #         self.errors.append(Self_Not_Target(node.row, node.col))
    #     else:    
    #         message = scope.is_variable_defined(node.identifier)
    #         self.errors += message
        
    #     expr_type = self.context.get_type(self.visit(node.expr, scope))
        
    #     if len(message) == 0:
    #         variable = scope.get_variable(node.identifier)
            
    #         if not expr_type.conformed_by(variable.vtype):
    #             if self.context.is_protocol_defined(node.vtype_token.lex):
    #                 protocol = self.context.get_protocol(variable.vtype)
    #                 if not expr_type.implements(protocol):
    #                     self.errors.append(Invalid_Initialize_type(node.identifier, variable.vtype, expr_type.name, node.expr.row, node.expr.col))
    #             else:
    #                 self.errors.append(Invalid_Initialize_type(node.identifier, variable.vtype, expr_type.name, node.expr.row, node.expr.col))
            
    #         return variable.vtype

    #     return "Object"
    
    # @visitor.when(DotNotationNode)
    # def visit(self, node: DotNotationNode, scope: Scope):
    #     type_name = self.visit(node.object, scope)
        
    #     if self.context.is_type_defined(type_name):
    #         object_type = self.context.get_type(type_name)
    #     else:
    #         object_type = self.context.get_protocol(type_name)
        
    #     inner_scope = Scope()
    #     inner_scope.is_dot_notation = True
    #     inner_scope.dot_notation_current_type = object_type
            
    #     print(inner_scope)
    #     return self.visit(node.member, inner_scope)
        
    @visitor.when(FuncCallNode)
    def visit(self, node: FuncCallNode, scope: Scope):
        function = None
        name_match = False
        param_match = False
        
        #if scope.is_dot_notation:
        #    name_match, param_match, return_match, function = scope.dot_notation_current_type.get_method(node.identifier, len(node.args_list), "Object", )
        #else:
        name_match, param_match = scope.is_function_defined(node.identifier.lex, len(node.args_list))
            
        if name_match:
            #if not scope.is_dot_notation:
            function = scope.get_function(node.identifier.lex)
            
            if not param_match:
                self.errors.append(Invalid_Arg_Count(node.identifier, len(function.params), len(node.args_list)))
            else:
                for i, arg in enumerate(node.args_list):
                    arg_type = self.visit(arg, scope)
                    print(function.params[i])
                    if not arg_type.match(function.params[i][1]):
                        self.errors.append(Invalid_Argument_Type(i, node.identifier.lex, function.params[i][1].name, arg_type.name, node.identifier.row, node.identifier.column))
            
            return function.return_type
        else:
            #if scope.is_dot_notation:
            #    self.errors.append(Not_Defined_In("Function", node.identifier, scope.dot_notation_current_type.name, node.row, node.col))
            #else:
            self.errors.append(Not_Defined("Function", node.identifier))
            return self.context.get_type("Object")[1]
        
    @visitor.when(ConstantNode)
    def visit(self, node:ConstantNode, scope):
        #solo es Number, String, Boolean por definicion luego no hay que comprobar
        succes, type = self.context.get(node.type)
        return type
    
    @visitor.when(VariableNode)
    def visit(self, node:VariableNode, scope: Scope):
        if scope.is_variable_defined(node.lex.lex):
            return scope.get_variable(node.lex.lex).vtype
        else:
            self.errors.append(Not_Defined("Variable", node.lex))
            
        #TODO activar cuando este ready el dot notation
        #else:
        #    if scope.is_dot_notation:
        #       self.errors.append(Not_Defined_In("Variable", node.lex, scope.#dot_notation_current_type.name, node.row, node.col))
        #    else:
        #        self.errors.append(Not_Defined("Variable", node.lex))
          
        return self.context.get_type("Object")[1]
                
    # @visitor.when(NewInstanceNode)
    # def visit(self, node:NewInstanceNode, scope: Scope):  
    #     if self.context.is_type_defined(node.identifier):
    #         type = self.context.get_type(node.identifier)
    #         params = type.get_params()
            
    #         if len(params) != len(node.args_list):
    #             self.errors.append(Invalid_Arg_Count(node.identifier, len(params), len(node.args_list)))
    #         else:    
    #             for i, arg in enumerate(node.args_list): 
    #                 arg_type = self.context.get_type(self.visit(arg, scope))
    #                 if not arg_type.conformed_by(params[i][1]):
    #                     self.errors.append(Invalid_Argument_Type(i, node.identifier, params[i][1], arg_type.name, arg.row, arg.col))  
    #         return type.name
    #     else:
    #         self.errors.append(Not_Defined("Type", node.identifier))
            
    #     return "Object"