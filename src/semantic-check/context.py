class Context:
    def __init__(self, parent = None) -> None:
        self.parent = parent
        self.variables = set()
        self.functions = {}
        
    def IsDefine(self, variable):
        return variable in self.variables or (self.parent != None and self.parent.IsDefine(variable))
    
    def IsDefine(self, function, args):
        if function in self.functions and len(self.functions[function]) == args:
            return True
        else:
            return self.parent != None and self.parent.IsDefined(function, args)
    
    def Define(self, variable):
        size = len(self.variables)
        self.variables.add(variable)
        return size == len(self.variables)
    
    def Define(self, function, args):
        if function in self.functions:
            return False
        
        self.functions[function] = args
        return True

    def CreateChildContext(self):
        return Context(self)
    
