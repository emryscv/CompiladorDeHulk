import utils.visitor as visitor
from  utils.utils import Token
from  grammars.HULK_grammar import *

class Node:
    def __init__(self) -> None:
        pass

class ProgramNode(Node):
    def __init__(self, definitions, mainExpression):
        super().__init__()
        self.definitions = definitions
        self.mainExpression = mainExpression

### high-level declarations and definitions ###
class DeclarationNode(Node):
    def __init__(self, identifier) -> None:
        super().__init__()
        self.identifier = identifier
        
class TypeDefNode(DeclarationNode):
    def __init__(self, identifier, optional_params, base_identifier, optional_base_args, body):
        super().__init__(identifier)
        self.optional_params = optional_params
        self.base_identifier = base_identifier
        self.optional_base_args = optional_base_args
        self.body = body

class ProtocolDefNode(DeclarationNode):
    def __init__(self, identifier, base_identifier, body):
        super().__init__(identifier)
        self.base_identifier = base_identifier
        self.body = body

class FuncDecNode(DeclarationNode):
    def __init__(self, identifier, params_list, return_type_token):
        super().__init__(identifier)
        self.params_list = params_list
        self.return_type_token = return_type_token
        
class FuncDefNode(FuncDecNode):
    def __init__(self, identifier, params_list, return_type_token, body):
        super().__init__(identifier, params_list, return_type_token)
        self.body = body

class MethodDefNode(FuncDefNode):
    def __init__(self, identifier, params_list, return_type_token, body):
        super().__init__(identifier, params_list, return_type_token, body)

### expressions ###
class ExpressionNode(Node):
    pass

class BlockExprNode(ExpressionNode):
    def __init__(self, expr_list):
        super().__init__()
        self.expr_list = expr_list

class LetInNode(ExpressionNode):
    def __init__(self, var_list, body):
        super().__init__()        
        self.var_list = var_list
        self.body = body

class VarDefNode(DeclarationNode):
    def __init__(self, identifier, vtype_token, expr):
        super().__init__(identifier)     
        self.vtype_token = vtype_token
        self.expr = expr
        
class AttributeDefNode(VarDefNode):
    pass     
    
class IfElseNode(ExpressionNode):
    def __init__(self, boolExpr_List, body_List):
        super().__init__()
        self.boolExpr_List = boolExpr_List
        self.body_List = body_List

class WhileLoopNode(ExpressionNode):
    def __init__(self, condition, body):
        super().__init__()
        self.condition = condition
        self.body = body

class ForLoopNode(LetInNode):
     def __init__(self, var, var_type_token, iterable, body):
         iter = VarDefNode(Token("iterable", id, iterable.identifier.row, iterable.identifier.column), Token("Iterable", id, iterable.identifier.row, iterable.identifier.column), iterable)
         condition = DotNotationNode(iter, FuncCallNode(Token("next", id, iterable.identifier.row, iterable.identifier.column), []))
         whileLoop = WhileLoopNode(condition, LetInNode([VarDefNode(var, var_type_token, DotNotationNode(VariableNode(Token("iterable", id, var.row, var.column)), FuncCallNode(Token("current", id, var.row, var.column), [])))], body))
         
         super().__init__([iter], whileLoop)
         
class BinaryOperationNode(ExpressionNode):
    def __init__(self, left, right, operator):
        super().__init__()
        self.operator = operator
        self.left = left
        self.right = right
        
class BooleanExprNode(BinaryOperationNode):
    def __init__(self, left, right, operator):
        super().__init__(left, right, operator)
    
    #when typing validate left and right most be bool#

class VarReAsignNode(ExpressionNode):
    def __init__(self, identifier, expr):
        super().__init__()
        self.identifier = identifier
        self.expr = expr

class DotNotationNode(ExpressionNode):
    def __init__(self, object, member):
        super().__init__()
        self.object = object
        self.member = member

class FuncCallNode(ExpressionNode):
    def __init__(self, identifier, args_list):
        super().__init__()
        self.identifier = identifier
        self.args_list = args_list

class AtomicNode(ExpressionNode):
    def __init__(self, lex):
        super().__init__()
        self.lex = lex
        
class ConstantNode(AtomicNode):
    def __init__(self, lex, type):
        super().__init__(lex)
        self.type = type

class VariableNode(AtomicNode):
    pass

class NewInstanceNode(ExpressionNode):
    def __init__(self, identifier, args_list):
        super().__init__()
        self.identifier = identifier
        self.args_list = args_list
