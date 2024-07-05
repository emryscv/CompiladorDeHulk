import utils.visitor as visitor
from  ast_nodes.hulk_ast_nodes import *

class SemeanticChecker(object):
    def __init__(self, errors, context):
        self.errors = errors
        self.context = context
    
    @visitor.on('node')
    def visit(self, node, scope):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node, scope):
        for definition in node.definitions: 
            self.visit(definition, scope.create_child_scope())

        self.visit(node.mainExpression, scope)

    # @visitor.when(TypeDefNode)
    # def visit(self, node, scope):
    #     type = self.context.get_type(node.identifier)
    #     for attribute in type.attributes:
    #         scope.define_variable(attribute.name, attribute.vtype)
            
    #     for method in type.methods:
    #         scope.define_method(method.name, method.params, method.return_type)
        
    #     #TODO añadir self y base
        
    #     for definition in node.body:
    #         self.visit(definition, scope)
            
    @visitor.when(FuncDefNode)
    def visit(self, node, scope):
        if node.return_type and not node.return_type in self.context.types: #TODO arreglar esta vaina
                self.errors.append(f'Type "{node.return_type}" is not defined.')
                
        for param in node.params_list:
            if not param[1] in self.context.types: #TODO arreglar esta vaina
                self.errors.append(f'Type "{node.return_type}" is not defined.')
            scope.define_variable(param[0], param[1])
        
        self.visit(node.body, scope)

    @visitor.when(BlockExprNode)
    def visit(self, node, scope):
        for i, expr in enumerate(node.expr_list):
            expr_type = self.visit(expr, scope)
            if i == len(node.expr_list) - 1:
                return expr_type
            
    @visitor.when(LetInNode)
    def visit(self, node, scope):
        inner_scope = scope.create_child_scope()
        
        for var in node.var_list: 
            self.visit(var, inner_scope)
            
        return self.visit(node.body, inner_scope)
    
    @visitor.when(VarDefNode)
    def visit(self, node, scope):
        self.errors += scope.define_variable(node.identifier, node.vtype, check=False)
        
        expr_type = self.visit(node.expr, scope)
        
        if node.vtype:
            if not node.vtype in self.context.types: #TODO arreglar esta vaina
                self.errors.append(f'Type "{node.vtype}" is not defined.')
            if node.vtype != expr_type:
                self.errors.append(f'Variable: ({node.identifier}) has type {node.vtype} and {expr_type} was given')
            return node.vtype
        else:
            scope.get_variable(node.identifier).vtype = expr_type
            return expr_type
            
    @visitor.when(IfElseNode)
    def visit(self, node, scope):
        for expr in node.boolExpr_List:
            self.visit(expr, scope)

        for expr in node.body_List:
            self.visit(expr, scope)
        
    @visitor.when(WhileLoopNode)
    def visit(self, node, scope):
        condition_type = self.visit(node.condition, scope)
        if not condition_type == "Boolean":
            self.errors.append(f'Boolean expression expected but {condition_type} was given')

        return self.visit(node.body, scope) #TODO esta vaina tiene q retornar lo de la ultima iteracion o None
    
    @visitor.when(BinaryOperationNode)
    def visit(self, node, scope):
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)

        if node.operator in ['+', '-', '*', '/', '^', '**']:
            if not (left_type == "Number" and right_type == "Number"):
                self.errors.append(f'Operator: ({node.operator}) can\' be applied to {left_type} and {right_type}')
                return None
            else:
                return "Number"
        elif node.operator in ['@', '@@']:
            if not (left_type in ["Number", "String", "Boolean"] and right_type  in ["Number", "String", "Boolean"]):
                self.errors.append(f'Operator: ({node.operator}) can\' be applied to {left_type} and {right_type}')
                return None
            else:
                return "String"
    
    @visitor.when(BooleanExprNode)
    def visit(self, node, scope):
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)
        
        if node.operator in ['<', '>', '<=', '>=', '==', '!='] and not (left_type == "Number" and right_type == "Number"):
                self.errors.append(f'Operator: ({node.operator}) can\'t be applied to {left_type} and {right_type}')
                return None
        elif node.operator in ['&', '|'] and not (left_type == "Boolean" and right_type == "Boolean"):
                self.errors.append(f'Operator: ({node.operator}) can\'t be applied to {left_type} and {right_type}')
                return None
        
        return "Boolean"
    
    @visitor.when(VarReAsignNode)
    def visit(self, node, scope):
        message = scope.is_variable_defined(node.identifier)
        self.errors += message
        
        expr_type = self.visit(node.expr, scope)
        
        if len(message) == 0:
            variable = scope.get_variable(node.identifier)
            if variable.vtype != expr_type:
                self.errors.append(f'Variable: ({node.identifier}) has type {variable.vtype} and {expr_type} was given')
            return variable.vtype

        return None
            
    @visitor.when(FuncCallNode)
    def visit(self, node, scope):
        message = scope.is_function_defined(node.identifier, len(node.arg_list))
        self.errors += message
        
        if len(message) == 0:
            function = scope.get_function(node.identifier)
        
        for i, arg in enumerate(node.arg_list):
            arg_type = self.visit(arg, scope)
            if len(message) == 0 and function.params[i][1] != arg_type:
                self.errors.append(f'Argument number: {i} in ({node.identifier}) has type ({function.params[i][1]}) but ({arg_type}) was given.')
                
        return function.return_type

    @visitor.when(AtomicNode)
    def visit(self, node, scope):
        if not node.type in self.context.types: #TODO arreglar esta vaina
            self.errors.append(f'Type "{node.type}" is not defined.')
        return node.type
    
    @visitor.when(VariableNode)
    def visit(self, node, scope):
        message = scope.is_variable_defined(node.lex)
        self.errors += message
        
        if len(message) == 0:
            return scope.get_variable(node.lex).vtype
        
        return None #TODO ver como hacemos con los errores aqui
                
            