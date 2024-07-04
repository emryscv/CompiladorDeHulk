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

    @visitor.when(TypeDefNode)
    def visit(self, node, scope):
        pass
    
    @visitor.when(BlockExprNode)
    def visit(self, node, scope):
        for expr in node.expr_list:
            self.visit(expr, scope)
            
    @visitor.when(LetInNode)
    def visit(self, node, scope):
        inner_scope = scope.create_child_scope()
        
        for var in node.var_list: 
            self.visit(var, inner_scope)
            
        self.visit(node.body, inner_scope)
    
    @visitor.when(VarDefNode)
    def visit(self, node, scope):
        self.errors += scope.define(node.identifier, node.type, check=False)
        
        if node.type and not node.type in self.context.types: #TODO arreglar esta vaina
                self.errors.append(f'Type "{node.type}" is not defined.')
        
        self.visit(node.expr, scope)
        
    @visitor.when(IfElseNode)
    def visit(self, node, scope):
        for expr in node.boolExpr_List:
            self.visit(expr, scope)

        for expr in node.body_List:
            self.visit(expr, scope)
        
    @visitor.when(WhileLoopNode)
    def visit(self, node, scope):
        self.visit(node.condition, scope)
        self.visit(node.body, scope)
    
    @visitor.when(BinaryOperationNode)
    def visit(self, node, scope):
        self.visit(node.left, scope)
        self.visit(node.right, scope)
    
    @visitor.when(VarReAsignNode)
    def visit(self, node, scope):
        self.errors += scope.is_defined(node.identifier)
        self.visit(node.expr, scope)
        
    @visitor.when(FuncCallNode)
    def visit(self, node, scope):
        self.errors += scope.is_defined(node.identifier, len(node.arg_list))
        
        for arg in node.arg_list:
            self.visit(arg, scope)
        
    @visitor.when(AtomicNode)
    def visit(self, node, scope):
        if node.type and not node.type in self.context.types: #TODO arreglar esta vaina
                self.errors.append(f'Type "{node.type}" is not defined.')
                
            