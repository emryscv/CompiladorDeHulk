import utils.visitor as visitor
import math
import random
from ast_nodes.hulk_ast_nodes import *
from semantic_check.Scope import Scope

class Interpreter:
    def __init__(self,context):
        self.context = context
        self.built_in_functions = {
            "print": lambda x: print(x[0]),
            "sen": lambda x: math.sin(x[0]),
            "cos": lambda x: math.cos(x[0]),
            "tan": lambda x: math.tan(x[0]),
            "sqrt": lambda x: math.sqrt(x[0]),
            "exp": lambda x: x[0]**x[1],
            "log": lambda x: math.log(x[0], x[1]),
            "rand": lambda x: random.random,
            "range": lambda x: (list(range(x[0], x[1])), x[1] - 1, - 1),
            "current": lambda x: x[0][x[1]], 
            "next": lambda x: (x[0], x[1], x[2] + 1) 
        }

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):

        program_scope = Scope()

        for definition in node.definitions:
            self.visit(definition, program_scope)
        self.visit(node.mainExpression, program_scope)
        
    @visitor.when(DeclarationNode)
    def visit(self, node, scope):
        pass

    @visitor.when(TypeDefNode)
    def visit(self, node, scope):
        pass

    @visitor.when(ProtocolDefNode)
    def visit(self, node, scope):
        pass

    @visitor.when(FuncDecNode)
    def visit(self, node, scope):
        pass

    @visitor.when(FuncDefNode)
    def visit(self, node, scope):
        scope.define_function(node.identifier.lex, [param[0].lex for param in node.params_list], node.return_type, node.body)

    @visitor.when(ExpressionNode)
    def visit(self, node, scope):
        pass

    @visitor.when(BlockExprNode)
    def visit(self, node, scope):
        for expr in node.expr_list:
            result = self.visit(expr, scope)
        return result

    @visitor.when(LetInNode)
    def visit(self, node, scope):
        child_scope = scope.create_child_scope()
        for var in node.var_list:
            self.visit(var, child_scope)
        return self.visit(node.body, child_scope)

    @visitor.when(VarDefNode)
    def visit(self, node, scope):
        value = self.visit(node.expr, scope)
        scope.define_variable(node.identifier.lex, node.identifier.token_type, True, value=value)

    @visitor.when(IfElseNode)
    def visit(self, node, scope):
        for i  in range(len(node.boolExpr_List)):
            condition = self.visit(node.boolExpr_List[i], scope)
            if condition:
                expr = self.visit(node.body_List[i], scope)
                return expr
           
        return self.visit(node.body_List[-1], scope)
        

    @visitor.when(WhileLoopNode)
    def visit(self, node, scope):
        while_scope = scope.create_child_scope()
        condition = self.visit(node.condition, while_scope)
        while condition:
            self.visit(node.body, while_scope)
            condition = self.visit(node.condition, while_scope)

    @visitor.when(ForLoopNode)
    def visit(self, node, scope):
        for_scope = scope.create_child_scope()
        for var in node.var_list:
            self.visit(var, for_scope)
        return self.visit(node.body, for_scope)

    @visitor.when(BinaryOperationNode)
    def visit(self, node, scope):
        right = self.visit(node.right, scope)
        left = self.visit(node.left, scope)
        sol = 0
        match node.operator.lex:
            case '+' | '@':
                sol = left + right
            case '-':
                sol = left - right
            case '*':
                sol = left * right
            case '/': 
                sol = left / right
            case '@@':
                sol = left + ' ' + right
            case '^':
                sol = left ** right
        return sol

    @visitor.when(BooleanExprNode)
    def visit(self, node, scope):
        right = self.visit(node.right, scope)
        left = self.visit(node.left, scope)
        sol = False
        match node.operator.lex:
            case '&':
                sol = left and right
            case '|':
                sol = left or right
            case '<':
                sol = left < right
            case '>': 
                sol = left > right
            case '<=':
                sol = left <= right
            case '>=':
                sol = left >= right
            case '!=':
                sol = not left == right
            case '==':
                sol = left == right
        return sol

    @visitor.when(VarReAsignNode)
    def visit(self, node, scope):
        value = self.visit(node.expr, scope)
        scope.define_variable(node.identifier.lex, check=False, value=value)
        return value

    @visitor.when(DotNotationNode)
    def visit(self, node, scope):
        self.visit(node.object, scope)
        return self.visit(node.member, scope)
    
    @visitor.when(FuncCallNode)
    def visit(self, node, scope):
        args = [self.visit(arg, scope) for arg in node.arg_list]
        if node.identifier.lex in self.built_in_functions:
            
            if node.identifier.lex == "next":
                iterable = scope.get_variable("iterable").value
                scope.define_variable("iterable", "Iterable", False, self.built_in_functions[node.identifier.lex](iterable))
                if iterable[1] > iterable[2] + 1:
                    return True
                else:
                    return False
                
            elif node.identifier.lex == "current":
                iterable = scope.get_variable("iterable").value
                return self.built_in_functions[node.identifier.lex]((iterable[0], iterable[2]))
            
            else:
                return self.built_in_functions[node.identifier.lex](args)

        else:
            function = scope.get_function(node.identifier.lex)
            call_scope = scope.create_child_scope()
            for i in range(len(function.params)):
                call_scope.define_variable(function.params[i], value=args[i])
            return self.visit(function.body, call_scope)
        
    @visitor.when(AtomicNode)
    def visit(self, node, scope):
        pass

    @visitor.when(ConstantNode)
    def visit(self, node, scope):
        if node.type == 'Number':
            if '.' in node.lex.lex:
                return float(node.lex.lex)
            else:
                return int(node.lex.lex)
        if node.type == 'Boolean':
            match node.lex.lex:
                case 'true':
                    return True
                case 'false':
                    return False
        return str(node.lex.lex)
        
    @visitor.when(VariableNode)
    def visit(self, node, scope):
        var = scope.get_variable(node.lex.lex)
        return var.value
    
    @visitor.when(NewInstanceNode)
    def visit(self, node, scope):
        pass