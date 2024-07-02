import utils.visitor as visitor
from  ast_nodes.hulk_ast_nodes import *

class FormatVisitor(object):
    @visitor.on('node')
    def visit(self, node, tabs):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ProgramNode [<definition>; ... <definition>;] expr;'
        statements = '\n'.join(self.visit(definition, tabs + 1) for definition in node.definitions)
        return f'{ans}\n{statements}\n{self.visit(node.mainExpression, tabs + 1)}'
    
    @visitor.when(FuncDecNode)
    def visit(self, node, tabs=0):
        params = ', '.join(node.args_list)
        ans = '\t' * tabs + f'\\__FuncDeclarationNode: def {node.identifier}  : {node.type_annotation} ({params}) -> <expr>'
        body = self.visit(node.body, tabs + 1)
        return f'{ans}\n{body}'
    
    @visitor.when(LetInNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__LetInNode: let [<var-def>, ... ,<var-def>] in <expr>'
        var_defs = '\n'.join(self.visit(var_def, tabs + 1) for var_def in node.var_list)
        body = self.visit(node.body, tabs + 1)
        
        return f'{ans}\n{var_defs}\n{body}'
    
    @visitor.when(VarDefNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__VarDefNode: {node.identifier}: {node.type_annotation} = <expr>'
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{expr}'
    
    @visitor.when(FuncCallNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__FuncCallNode: {node.identifier}(<expr>, ..., <expr>)'
        args = '\n'.join(self.visit(arg, tabs + 1) for arg in node.arg_list)
        
        return f'{ans}\n{args}'

    @visitor.when(BinaryOperationNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ {node.__class__.__name__}: <expr> {node.operator} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(AtomicNode)
    def visit(self, node, tabs=0):
        return '\t' * tabs + f'\\__ {node.__class__.__name__}: {node.lex}'
    