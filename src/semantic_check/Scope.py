from semantic_check.utils.Variable import Variable
from semantic_check.utils.Function import Function

class Scope:
    def __init__(self, parent = None):
        self.parent: Scope = parent
        self.variables = {}
        self.functions = {"print": Function("print", [("string", "String")], "Object")}
        
    def is_variable_defined(self, vname:str):
        return [] if vname in self.variables or (self.parent != None and self.parent.IsDefine(vname)) else [f'Variable "{vname}" is not defined.']
    
    def is_function_defined(self, fname:str, args):
        if fname in self.functions:
            if len(self.functions[fname].params) == args:
                return []
            else:
                return [f'Function ({fname}): {len(self.functions[fname].params)} params expected but {args} were given.']
        elif self.parent != None:
            return self.parent.IsDefine(fname, args)
        else:
            return [f'Function "{fname}" is not defined.']
        
    def define_variable(self, vname:str, vtype=None, check=True):
        if check and vname in self.variables:
            return [f'Variable with the same name ({vname}) is already defined']
        
        self.variables[vname] = Variable(vname, vtype)
        return []
    
    def define_function(self, fname, params, return_type):
        if fname in self.functions:
            return [f'Function with the same name ({fname}) is already defined']
        
        self.functions[fname] = Function(fname, params, return_type)
        return []
        
    def get_variable(self, vname:str):
        try:
            return self.variables[vname]
        except KeyError:
            return self.parent.get_variable(vname)
        
    def get_function(self, fname:str):
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