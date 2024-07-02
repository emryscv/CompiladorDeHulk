from ast_nodes.ast_base_nodes import BinaryNode, AtomicNode, Node
import utils.visitor as visitor

class ConstantNode(AtomicNode):
    def validate(self, context):
        return True

class VariableNode(AtomicNode):
    def validate(self, context):
        return context.IsDefine(self.lex)

class BinaryOperationNode(BinaryNode):
    def __init__(self, left, right, operator):
        super().__init__(left, right)
        self.operator = operator
        
    def validate(self, context):
        return self.left.validate(context) and self.right.validate(context)

class BlockExprNode(Node):
    def __init__(self, expr_list):
        super().__init__()
        self.expr_list = expr_list
    
    def validate(self, context):
        for expr in self.expr_list:
            if not expr.validate(context):
                return False
        return True
    
class FuncCallNode(Node):
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
    
class FuncDecNode(Node):
    def __init__(self, identifier, args_list, type_annotation):
        super().__init__()
        self.identifier = identifier
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

class IfElseNode(Node):
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

class BooleanExprNode(BinaryOperationNode):
    def __init__(self, left, right, operator):
        super().__init__(left, right, operator)
    
    #when typing validate left and right most be bool#

class LetInNode(Node):
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

class VarDefNode(Node):
    def __init__(self, identifier, type_annotation, expr):
        super().__init__()        
        self.identifier = identifier
        self.type_annotation = type_annotation
        self.expr = expr
    
    def validate(self, context):

        return self.expr.validate(context) and context.define(self.identifier)

class VarReAsignNode(Node):
    def __init__(self, identifier, expr):
        super().__init__()
        self.identifier = identifier
        self.expr = expr
    
    def validate(self, context):
        return context.IsDefine(self.identifier) and self.expr.validate(context) 

class DotNotationNode(Node):
    def __init__(self, object, member):
        super().__init__()
        self.object = object
        self.member = member
        
class ProgramNode(Node):
    def __init__(self, declarations, mainExpression):
        super().__init__()
        self.declarations = declarations
        self.mainExpression = mainExpression

class TypeDefNode(Node):
    def __init__(self, identifier, optional_args, base_identifier, base_optional_args, body):
        super().__init__()
        self.identifier = identifier
        self.optional_args = optional_args
        self.base_identifier = base_identifier
        self.base_optional_args = base_optional_args
        self.body = body
    
class NewInstanceNode(Node):
    def __init__(self, identifier, expr):
        super().__init__()
        self.identifier = identifier
        self.expr = expr

class ProtocolDefNode(Node):
    def __init__(self, identifier, base_identifier, body):
        super().__init__()
        self.identifier = identifier
        self.base_identifier = base_identifier
        self.body = body

class WhileLoopNode(Node):
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



def get_printer(AtomicNode=AtomicNode, BinaryNode=BinaryOperationNode, FuncCallNode=FuncCallNode):

    class PrintVisitor(object):
        @visitor.on('node')
        def visit(self, node, tabs):
            pass

        @visitor.when(BinaryNode)
        def visit(self, node, tabs=0):
            ans = '\t' * tabs + f'\\__<expr> {node.__class__.__name__}  {node.operator} <expr>'
            left = self.visit(node.left, tabs + 1)
            right = self.visit(node.right, tabs + 1)
            return f'{ans}\n{left}\n{right}'

        @visitor.when(AtomicNode)
        def visit(self, node, tabs=0):
                
            return '\t' * tabs + f'\\__ {node.__class__.__name__}: {node.lex}'

        
        @visitor.when(FuncCallNode)
        def visit(self, node, tabs=0):
            arg = ""
            for expr in node.arg_list:
               arg += self.visit(expr, tabs+1) + f'\n {"\t" * (tabs+1)};\n'
            return '\t' * tabs + f'\\__ {node.__class__.__name__}: {node.identifier} args: {{ \n   {arg}{"\t" * tabs}}}'

    printer = PrintVisitor()
    return (lambda ast: printer.visit(ast))