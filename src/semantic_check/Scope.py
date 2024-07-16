from semantic_check.utils.Variable import Variable
from semantic_check.utils.Function import Function
from semantic_check.utils.Type import Type

class Scope:
    def __init__(self, parent = None):
        self.parent: Scope = parent
        self.variables = {}
        self.functions = {}
        self.is_self_asignable:bool  = False
        self.is_dot_notation:bool = False
        self.dot_notation_current_type:Type = None
        self.methods = {}
        self.type_deep = {}
        
    def is_variable_defined(self, vname:str):
        return vname in self.variables or (self.parent != None and self.parent.is_variable_defined(vname))
    
    def  is_function_defined(self, fname:str, args):
        if fname in self.functions:
            if len(self.functions[fname].params) == args:
                return (True, True)
            else:
                return (True, False)
        elif self.parent != None:
            return self.parent.is_function_defined(fname, args)
        else:
            return (False, False)
        
    def define_variable(self, vname:str, vtype=None, check=True, value=None, reasign=False):

        if reasign:
            self.variables[vname] = Variable(vname, vtype, value)
            return True
        
        if check and vname in self.variables:
            return False
        
        self.variables[vname] = Variable(vname, vtype, value)
        return True
        
    def define_function(self, fname, params, return_type, function_body=None, check=True):
        if check:
            if fname in self.functions:
                return True
        
        self.functions[fname] = Function(fname, params, return_type, function_body)
        return False
    
    def define_method(self, mname, params, return_type, function_body):
        if mname in self.methods:
            self.type_deep[mname] += 1
            self.methods[mname].append(Function(mname, params, return_type, function_body))
        else:
            self.type_deep[mname] = 0
            self.methods[mname] = [Function(mname, params, return_type, function_body)]
        
    def get_variable(self, vname:str) -> Variable:
        try:
            return self.variables[vname]
        except KeyError:
            return self.parent.get_variable(vname)
        
    def get_function(self, fname:str) -> Function:
        try:
            return self.functions[fname]
        except KeyError:
            return self.parent.get_function(fname)
        
    def get_method(self, mname, is_base=False):
        if is_base:
            self.type_deep[mname] -= 1
        try:
            return self.methods[mname][self.type_deep[mname]]
        except KeyError:
            return self.parent.methods.get_method(mname)
    
    def reset_type_deep(self, mname):
        self.type_deep[mname] += 1
        
    def create_child_scope(self):
        return Scope(self)
    
    def __str__(self):
        return '{\n\t' + '\n\t'.join(y for x in self.functions.values() for y in str(x).split('\n')) + '\n\t' + '\n\t'.join(y for x in self.variables.values() for y in str(x).split('\n')) + '\n}'

    def __repr__(self):
        return str(self)