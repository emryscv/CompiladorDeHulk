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
            "range": lambda x: (list(range(x[0], x[1])), x[1], - 1),
            "current": lambda x: x[0][x[1]], 
            "next": lambda x: (x[0], x[1], x[2] + 1) 
        }
        self.types = {}
        self.current_function = None

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
        type = self.context.get_type(node.identifier.lex)
        self.types[type[1].name] = node

    @visitor.when(ProtocolDefNode)
    def visit(self, node, scope):
        pass

    @visitor.when(FuncDecNode)
    def visit(self, node, scope):
        pass

    @visitor.when(FuncDefNode)
    def visit(self, node, scope):
        scope.define_function(node.identifier.lex, [param[0] for param in node.params_list], node.return_type_token, node.body)

    @visitor.when(MethodDefNode)
    def visit(self, node, scope):
        scope.define_method(node.identifier.lex, [param[0] for param in node.params_list], node.return_type_token, node.body)

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
            scope.define_variable(node.identifier.lex, node.expr.identifier.lex, True, value=value)
        else:
            scope.define_variable(node.identifier.lex, node.vtype_token, True, value=value)

    @visitor.when(IfElseNode)
    def visit(self, node, scope):
        for i  in range(len(node.boolExpr_List)):
            condition = self.visit(node.boolExpr_List[i][1], scope)
            if condition:
                expr = self.visit(node.body_List[i][1], scope)
                return expr
        else:
            return self.visit(node.body_List[-1][1], scope)
        

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
        match node.operator.lex:
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
            case '%':
                sol = left % right
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
            is_method = False
            is_base = False
            actual_func = None
            if node.identifier.lex == 'base':
                actual_func = self.current_function
                function = scope.get_method(self.current_function, True)
                is_method = True
                is_base = True
            else:
                self.current_function = node.identifier.lex
                try:
                    function = scope.get_function(node.identifier.lex)
                except:
                    function = scope.get_method(node.identifier.lex)
                    is_method = True
            call_scope = scope
            if not is_method:
                call_scope = scope.create_child_scope()
            for i in range(len(function.params)):
                call_scope.define_variable(function.params[i].lex, value=args[i])
            output = self.visit(function.body, call_scope)

            if is_base:
                scope.reset_type_deep(actual_func)
            return output
        
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
    def visit(self, node, scope, get_var_name=False):
        if node.lex.lex == 'self':
            return 'self'
        var = scope.get_variable(node.lex.lex)
        if get_var_name:
            return var.name
        return var.value
    
    @visitor.when(NewInstanceNode)
    def visit(self, node, scope):
        var_type = self.context.get_type(node.identifier.lex)
        args = [self.visit(arg, scope) for arg in node.args_list]
        instance = self.types[var_type[1].name]

        parent = None
        parent_args = None
        if instance.optional_params:
            for i in range(len(instance.optional_params)):
                parameter_type = instance.optional_params[i][1]
                if parameter_type:
                    parameter_type = parameter_type.lex
                
                scope.define_variable(instance.optional_params[i][0].lex, instance.optional_params[i][1], value = args[i])

            if instance.optional_base_args:
                parent_args = instance.optional_base_args
        
        if var_type[1].parent and not var_type[1].parent.name == 'Object':
            parent = self.types[var_type[1].parent.name]
            if parent_args:
                args = parent_args
            else:
                args = node.args_list
            parent_instance = NewInstanceNode(parent.identifier, args)
            self.visit(parent_instance, scope)
        print(node.identifier)
        for expr in instance.body:
            self.visit(expr, scope)