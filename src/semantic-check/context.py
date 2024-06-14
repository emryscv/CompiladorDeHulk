class Context:
    def __init__(self, parent = None) -> None:
        self.parent = parent
        self.variables = set()
        self.functions = {}
        
    def IsDefine(self, variable):
        return variable in self.variables or (self.parent != None and self.parent.IsDefine(variable))
    
    def IsDefine(self, function, args):
        if function in self.functions:
            if len(self.functions[function]) == args:
                return (True, True)
            else:
                return (True, False)
        elif self.parent != None:
            return self.parent.IsDefine(function, args)
        else:
            return (False, False)
        
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
    
