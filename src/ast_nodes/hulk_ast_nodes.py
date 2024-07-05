import utils.visitor as visitor

class Node:
    def __init__(self, row, col) -> None:
        pass

class ProgramNode(Node):
    def __init__(self, definitions, mainExpression):
        super().__init__(0, 0)
        self.definitions = definitions
        self.mainExpression = mainExpression

### high-level declarations and definitions ###
class DeclarationNode(Node):
    def __init__(self, identifier, row, col) -> None:
        super().__init__(row, col)
        self.identifier = identifier
        
class TypeDefNode(DeclarationNode):
    def __init__(self, identifier, optional_args, base_identifier, base_optional_args, body, row, col):
        super().__init__(identifier, row, col)
        self.optional_args = optional_args
        self.base_identifier = base_identifier
        self.base_optional_args = base_optional_args
        self.body = body

class ProtocolDefNode(DeclarationNode):
    def __init__(self, identifier, base_identifier, body, row, col):
        super().__init__(identifier, row, col)
        self.base_identifier = base_identifier
        self.body = body

class FuncDecNode(DeclarationNode):
    def __init__(self, identifier, params_list, return_type, row, col):
        super().__init__(identifier, row, col)
        self.params_list = params_list
        self.return_type = return_type
        
class FuncDefNode(FuncDecNode):
    def __init__(self, identifier, params_list, return_type, body, row, col):
        super().__init__(identifier, params_list, return_type, row, col)
        self.body = body

class MethodDefNode(FuncDefNode):
    def __init__(self, identifier, params_list, return_type, body, row, col):
        super().__init__(identifier, params_list, return_type, body, row, col)

### expressions ###
class ExpressionNode(Node):
    pass

class BlockExprNode(ExpressionNode):
    def __init__(self, expr_list, row, col):
        super().__init__(row, col)
        self.expr_list = expr_list

class LetInNode(ExpressionNode):
    def __init__(self, var_list, body, row, col):
        super().__init__(row, col)        
        self.var_list = var_list
        self.body = body

class VarDefNode(DeclarationNode):
    def __init__(self, identifier, vtype, expr, row, col):
        super().__init__(identifier, row, col)     
        self.vtype = vtype
        self.expr = expr
    
class IfElseNode(ExpressionNode):
    def __init__(self, boolExpr_List, body_List, row, col):
        super().__init__(row, col)
        self.boolExpr_List = boolExpr_List
        self.body_List = body_List

class WhileLoopNode(ExpressionNode):
    def __init__(self, condition, body, row, col):
        super().__init__(row, col)
        self.condition = condition
        self.body = body

class ForLoopNode(LetInNode): #TODO manejar correctament los row and cols
     def __init__(self, var, iterable, body, row, col):
         iter = VarDefNode("iterable", "Iterable", iterable, iterable.row, iterable.col)
         condition = DotNotationNode(iter, FuncCallNode("next", [], iter.row, iter.col), iter.row, iter.col)
         whileLoop = WhileLoopNode(condition, LetInNode([VarDefNode(var, "", DotNotationNode(VariableNode("iterable"), FuncCallNode("current", [])))], body))
         
         super().__init__([iter], whileLoop, row, col)
         
class BinaryOperationNode(ExpressionNode):
    def __init__(self, left, right, operator, row, col):
        super().__init__(row, col)
        self.operator = operator
        self.left = left
        self.right = right
        
class BooleanExprNode(BinaryOperationNode):
    def __init__(self, left, right, operator, row, col):
        super().__init__(left, right, operator, row, col)
    
    #when typing validate left and right most be bool#

class VarReAsignNode(ExpressionNode):
    def __init__(self, identifier, expr, row, col):
        super().__init__(row, col)
        self.identifier = identifier
        self.expr = expr

class DotNotationNode(ExpressionNode):
    def __init__(self, object, member, row, col):
        super().__init__(row, col)
        self.object = object
        self.member = member

class FuncCallNode(ExpressionNode):
    def __init__(self, identifier, arg_list, row, col):
        super().__init__(row, col)
        self.identifier = identifier
        self.arg_list = arg_list

class AtomicNode(ExpressionNode):
    def __init__(self, lex, row, col):
        super().__init__(row, col)
        self.lex = lex
        
class ConstantNode(AtomicNode):
    def __init__(self, lex, type, row, col):
        super().__init__(lex, row, col)
        self.type = type

class VariableNode(AtomicNode):
    pass

class NewInstanceNode(ExpressionNode):
    def __init__(self, identifier, expr_list, row, col):
        super().__init__(row, col)
        self.identifier = identifier
        self.expr_list = expr_list
