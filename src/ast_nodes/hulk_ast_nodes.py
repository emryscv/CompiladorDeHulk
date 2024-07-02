from ast_nodes.ast_base_nodes import Node
import utils.visitor as visitor

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
    def __init__(self, identifier, body):
        super().__init__(identifier)
        self.body = body

class FuncDecNode(DeclarationNode):
    def __init__(self, identifier, args_list, type_annotation):
        super().__init__(identifier)
        self.args_list = args_list
        self.type_annotation = type_annotation
        
class FuncDefNode(FuncDecNode):
    def __init__(self, identifier, args_list, type_annotation, body):
        super().__init__(identifier, args_list, type_annotation)
        self.body = body

    def validate(self, context):
        if not context.Define(self.identifier, self.args):
            return False
        
        innerContext = context.CreateChildContext()
        
        for arg in self.args_list:
            innerContext.Define(arg)
            
        return self.body.validate(innerContext)

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
    def __init__(self,var_list, body):
        super().__init__()        
        self.var_list = var_list
        self.body = body
    
    def validate(self, context):

        innerContext = context.CreateChildContext()

        for var in self.var_list:
            if not var.validate(innerContext):
                return False
        return self.body.validate(innerContext)

class VarDefNode(DeclarationNode):
    def __init__(self, identifier, type_annotation, expr):
        super().__init__(identifier)     
        self.type_annotation = type_annotation
        self.expr = expr
    
    def validate(self, context):

        return self.expr.validate(context) and context.define(self.identifier)
    
class IfElseNode(ExpressionNode):
    def __init__(self, boolExpr_List, body_List):
        super().__init__()
        self.boolExpr_lsit = boolExpr_List
        self.body_List = body_List
        
    def validate(self, context):
        for boolExpr in self.boolExpr_List:
            if not boolExpr.validate(context):
                return False
        
        for body in self.body_List:
            innerContext = context.CreateChildContext()
            if not body.validate(innerContext):
                return False
        
        return True

class WhileLoopNode(ExpressionNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def validate(self, context):
        if not self.condition.validate(context):
            return False
        
        innerContext = context.CreateChildContext()

        return self.body.evaluate(innerContext)

class ForLoopNode(LetInNode):
     def __init__(self, var, iterable, body):
         iter = VarDefNode("iterable", iterable)
         condition = DotNotationNode(iter, FuncCallNode("next", []))
         whileLoop = WhileLoopNode(condition, LetInNode([VarDefNode(var, DotNotationNode(iter, FuncCallNode("current", [])))], body))
         
         super().__init__([iter], whileLoop)
         
class BinaryOperationNode(ExpressionNode):
    def __init__(self, left, right, operator):
        self.operator = operator
        self.left = left
        self.right = right
        
    def validate(self, context):
        return self.left.validate(context) and self.right.validate(context)
        
class BooleanExprNode(BinaryOperationNode):
    def __init__(self, left, right, operator):
        super().__init__(left, right, operator)
    
    #when typing validate left and right most be bool#

class VarReAsignNode(ExpressionNode):
    def __init__(self, identifier, expr):
        super().__init__()
        self.identifier = identifier
        self.expr = expr
    
    def validate(self, context):
        return context.IsDefine(self.identifier) and self.expr.validate(context) 

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
    
    def validate(self, context):
        if context.IsDefine(self.identifier, len(self.arg_list)):
            for expr in self.arg_list:
                if not expr.validate(context):
                    return False    
            return True
        return False        

class AtomicNode(ExpressionNode):
    def __init__(self, lex):
        self.lex = lex
        
class ConstantNode(AtomicNode):
    def validate(self, context):
        return True

class VariableNode(AtomicNode):
    def validate(self, context):
        return context.IsDefine(self.lex)

class NewInstanceNode(ExpressionNode): #TODO ver si es function call
    def __init__(self, identifier, expr): #TODO expr es una lista de argumentos
        super().__init__()
        self.identifier = identifier
        self.expr = expr
