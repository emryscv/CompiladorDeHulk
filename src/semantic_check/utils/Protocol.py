from semantic_check.utils.Function import Function

class Protocol:
    def __init__(self, name: str):
        self.name = name
        self.methods: list[Function] = []
        self.parent: Protocol = None
        
    def declare_method(self, name:str, params:list, return_type:str):
        if name in (method.name for method in self.methods):
            return False

        method = Function(name, params, return_type)
        self.methods.append(method)
        return True
    
    def __str__(self):
        return f'{self.name}{(" extends " + self.parent.name) if self.parent else ""} {self.methods}'
    
    def __rep__(self):
        return self.__str__()