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
            "sin": lambda x: math.sin(x[0]),
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
        self.types = {}

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
        type = self.context.get_type(node.identifier)
        self.types[type.name] = node

    @visitor.when(ProtocolDefNode)
    def visit(self, node, scope):
        pass

    @visitor.when(FuncDecNode)
    def visit(self, node, scope):
        pass

    @visitor.when(FuncDefNode)
    def visit(self, node, scope):
        scope.define_function(node.identifier, [param[0] for param in node.params_list], node.return_type_token, node.body)

    @visitor.when(MethodDefNode)
    def visit(self, node, scope):
        scope.define_function(node.identifier, [param[0] for param in node.params_list], node.return_type_token, node.body, True, False)

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
        if isinstance(node.expr, NewInstanceNode):
            scope.define_variable(node.identifier, node.expr.identifier, True, value=value)
        else:
            scope.define_variable(node.identifier, node.vtype_token, True, value=value)

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
        sol = None
        match node.operator:
            case '+':
                sol = left + right
            case '-':
                sol = left - right
            case '*':
                sol = left * right
            case '/': 
                sol = left / right
            case '@':
                sol = str(left) + str(right)
            case '@@':
                sol = str(left) + " " + str(right)
            case '^':
                sol = left ** right
        return sol

    @visitor.when(BooleanExprNode)
    def visit(self, node, scope):
        right = self.visit(node.right, scope)
        left = self.visit(node.left, scope)
        sol = False
        match node.operator:
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
        scope.define_variable(node.identifier, check=False, value=value)
        return value

    @visitor.when(DotNotationNode)
    def visit(self, node, scope):
        obj = None
        if isinstance(node.object, VariableNode):
            obj = self.visit(node.object, scope, True)
        try:
            obj = scope.get_variable(obj)
        except:
            pass
        if obj and isinstance(node.member, FuncCallNode):
            return self.visit(node.member, scope, obj.vtype)
        else:
            self.visit(node.object, scope)
            return self.visit(node.member, scope)
            
    
    @visitor.when(FuncCallNode)
    def visit(self, node, scope, current_type=None):
        args = [self.visit(arg, scope) for arg in node.args_list]
        if node.identifier in self.built_in_functions:
            
            if node.identifier == "next":
                iterable = scope.get_variable("iterable").value
                scope.define_variable("iterable", "Iterable", False, self.built_in_functions[node.identifier](iterable))
                if iterable[1] > iterable[2] + 1:
                    return True
                else:
                    return False
                
            elif node.identifier == "current":
                iterable = scope.get_variable("iterable").value
                return self.built_in_functions[node.identifier]((iterable[0], iterable[2]))
            
            else:
                return self.built_in_functions[node.identifier](args)

        else:
            if node.identifier == 'base' or not node.identifier in scope.functions:
                print(node.identifier)
                print(1)
                print(current_type)
                var_type = self.context.get_type(current_type) 
                parent = self.types[var_type.parent.name]
                print(parent.body)
                for expr in parent.body:
                    self.visit(expr, scope)
            print(scope)
            function = scope.get_function(node.identifier)
            call_scope = scope
            if not function.is_method:
                call_scope = scope.create_child_scope()
            for i in range(len(function.params)):
                print('yes')
                call_scope.define_variable(function.params[i], value=args[i])
            return self.visit(function.body, call_scope)
        
    @visitor.when(AtomicNode)
    def visit(self, node, scope):
        pass

    @visitor.when(ConstantNode)
    def visit(self, node, scope):
        if node.type == 'Number':
            if '.' in node.lex:
                return float(node.lex)
            else:
                return int(node.lex)
        if node.type == 'Boolean':
            match node.lex:
                case 'true':
                    return True
                case 'false':
                    return False
        return str(node.lex)
        
    @visitor.when(VariableNode)
    def visit(self, node, scope, get_var_name=False):
        if node.lex == 'self':
            return 'self'
        var = scope.get_variable(node.lex)
        if get_var_name:
            return var.name
        return var.value
    
    @visitor.when(NewInstanceNode)
    def visit(self, node, scope, is_parent=False):
        var_type = self.context.get_type(node.identifier)
        args = [self.visit(arg, scope) for arg in node.args_list]
        instance = self.types[var_type.name]

        parent = None
        parent_args = None

        if instance.optional_params:
            for i in range(len(instance.optional_params)):
                scope.define_variable(instance.optional_params[i][0], instance.optional_params[i][1], value = args[i])

            if instance.optional_base_args:
                parent_args = instance.optional_base_args
        
        if var_type.parent and not var_type.parent.name == 'Object':
            parent = self.types[var_type.parent.name]
            if parent_args:
                args = parent_args
            else:
                args = node.args_list
            parent_instance = NewInstanceNode(parent.identifier, args, 0, 0)
            self.visit(parent_instance, scope, True)

        if not  is_parent:
            for expr in instance.body:
                self.visit(expr, scope)