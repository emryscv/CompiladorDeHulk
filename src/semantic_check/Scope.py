from Function import Function
from Variable import Variable

class Scope:
    def __init__(self, parent = None) -> None:
        self.parent = parent
        self.variables = {}
        self.functions = {}
        
    def IsDefine(self, vname):
        return vname in self.variables or (self.parent != None and self.parent.IsDefine(vname))
    
    def IsDefine(self, fname, args):
        if fname in self.functions:
            if len(self.functions[fname]) == args:
                return (True, True)
            else:
                return (True, False)
        elif self.parent != None:
            return self.parent.IsDefine(fname, args)
        else:
            return (False, False)
        
    def Define(self, vname, vtype=None):
        if vname in self.variables:
            return False
        
        self.variables[vname] = Variable(vname, vtype)
        return True
    
    def Define(self, fname, params, return_type):
        if fname in self.functions:
            return False
        
        self.functions[fname] = Function(fname, params, return_type)
        return True

    def CreateChildScope(self):
        return Scope(self)
    
