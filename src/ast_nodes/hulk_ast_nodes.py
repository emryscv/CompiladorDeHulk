import utils.visitor as visitor

class Node:
    def __init__(self, ) -> None:
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
    def __init__(self, identifier, optional_args, base_identifier, base_optional_args, body):
        super().__init__(identifier)
        self.optional_args = optional_args
        self.base_identifier = base_identifier
        self.base_optional_args = base_optional_args
        self.body = body

class ProtocolDefNode(DeclarationNode):
    def __init__(self, identifier, base_identifier, body):
        super().__init__(identifier)
        self.base_identifier = base_identifier
        self.body = body

class FuncDecNode(DeclarationNode):
    def __init__(self, identifier, params_list, return_type):
        super().__init__(identifier)
        self.params_list = params_list
        self.return_type = return_type
        
class FuncDefNode(FuncDecNode):
    def __init__(self, identifier, params_list, return_type, body):
        super().__init__(identifier, params_list, return_type)
        self.body = body

class MethodDefNode(FuncDefNode):
    def __init__(self, identifier, params_list, return_type, body):
        super().__init__(identifier, params_list, return_type, body)

### expressions ###
class ExpressionNode(Node):
    pass

class BlockExprNode(ExpressionNode):
    def __init__(self, expr_list):
        super().__init__()
        self.expr_list = expr_list
    
    def validate(self, context):
        for expr in self.expr_list:
            if not expr.validate(context):
                return False
        return True

class LetInNode(ExpressionNode):
    def __init__(self, var_list, body):
        super().__init__()        
        self.var_list = var_list
        self.body = body

class VarDefNode(DeclarationNode):
    def __init__(self, identifier, vtype, expr):
        super().__init__(identifier)     
        self.vtype = vtype
        self.expr = expr
    
class IfElseNode(ExpressionNode):
    def __init__(self, boolExpr_List, body_List):
        super().__init__()
        self.boolExpr_List = boolExpr_List
        self.body_List = body_List

class WhileLoopNode(ExpressionNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class ForLoopNode(LetInNode):
     def __init__(self, var, iterable, body):
         iter = VarDefNode("iterable", "Iterable", iterable)
         condition = DotNotationNode(iter, FuncCallNode("next", []))
         whileLoop = WhileLoopNode(condition, LetInNode([VarDefNode(var, "", DotNotationNode(VariableNode("iterable"), FuncCallNode("current", [])))], body))
         
         super().__init__([iter], whileLoop)
         
class BinaryOperationNode(ExpressionNode):
    def __init__(self, left, right, operator):
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
    def __init__(self, identifier, arg_list):
        super().__init__()
        self.identifier = identifier
        self.arg_list = arg_list

class AtomicNode(ExpressionNode):
    def __init__(self, lex):
        self.lex = lex
        
class ConstantNode(AtomicNode):
    def __init__(self, lex, type):
        super().__init__(lex)
        self.type = type

class VariableNode(AtomicNode):
    pass

class NewInstanceNode(ExpressionNode):
    def __init__(self, identifier, expr_list):
        super().__init__()
        self.identifier = identifier
        self.expr_list = expr_list
