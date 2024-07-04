from semantic_check.utils.Variable import Variable
from semantic_check.utils.Function import Function

class Scope:
    def __init__(self, parent = None):
        self.parent = parent
        self.variables = {}
        self.functions = {}
        
    def is_define(self, vname:str):
        return vname in self.variables or (self.parent != None and self.parent.IsDefine(vname))
    
    def is_define(self, fname:str, args):
        if fname in self.functions:
            if len(self.functions[fname]) == args:
                return (True, True)
            else:
                return (True, False)
        elif self.parent != None:
            return self.parent.IsDefine(fname, args)
        else:
            return (False, False)
        
    def define(self, vname:str, vtype=None):
        if vname in self.variables:
            return [f'Variable with the same name ({vname}) is already defined']
        
        self.variables[vname] = Variable(vname, vtype)
        return []
    
    def define(self, fname, params, return_type):
        if fname in self.functions:
            return [f'Function with the same name ({fname}) is already defined']
        
        self.functions[fname] = Function(fname, params, return_type)
        return []

    def create_child_scope(self):
        return Scope(self)
    
    def __str__(self):
        return '{\n\t' + '\n\t'.join(y for x in self.functions.values() for y in str(x).split('\n')) + '\n}'

    def __repr__(self):
        return str(self)