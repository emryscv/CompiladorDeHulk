from semantic_check.utils.Variable import Variable
from semantic_check.utils.Function import Function

class Scope:
    def __init__(self, parent = None):
        self.parent: Scope = parent
        self.variables = {}
        self.functions = {"print": Function("print", [("string", "Object")], "Object")}
        self.is_self_asignable:bool  = False
        
    def is_variable_defined(self, vname:str):
        return vname in self.variables or (self.parent != None and self.parent.is_variable_defined(vname))
    
    def is_function_defined(self, fname:str, args):
        if fname in self.functions:
            if len(self.functions[fname].params) == args:
                return (True, True)
            else:
                return (True, False)
        elif self.parent != None:
            return self.parent.is_function_defined(fname, args)
        else:
            return (False, False)
        
    def define_variable(self, vname:str, vtype=None, check=True, value=None):
        if check and vname in self.variables:
            return False
        
        self.variables[vname] = Variable(vname, vtype, value)
        return True
    
    def define_function(self, fname, params, return_type):
        if fname in self.functions:
            return True
        
        self.functions[fname] = Function(fname, params, return_type)
        return False
        
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
        
    def create_child_scope(self):
        return Scope(self)
    
    def __str__(self):
        return '{\n\t' + '\n\t'.join(y for x in self.functions.values() for y in str(x).split('\n')) + '\n\t' + '\n\t'.join(y for x in self.variables.values() for y in str(x).split('\n')) + '\n}'

    def __repr__(self):
        return str(self)