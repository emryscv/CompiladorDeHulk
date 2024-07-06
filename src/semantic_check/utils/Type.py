from semantic_check.utils.Function import Function
from semantic_check.utils.Variable import Variable
from semantic_check.utils.Protocol import Protocol

class Type:
    def __init__(self, name:str):
        self.name = name
        self.attributes: list[Variable] = []
        self.methods = []
        self.params = []
        self.parent: Type = None
    
    def define_method(self, name:str, params:list, return_type:str):
        if name in (method.name for method in self.methods):
            return False
        
        method = Function(name, params, return_type)
        self.methods.append(method)
        return True
    
    def define_attribute(self, name:str, typex:str):    
        if name in (attribute.name for attribute in self.attributes):
            return False

        attribute = Variable(name, typex)
        self.attributes.append(attribute)
        return True
    
    def get_method(self, name, params_count, return_type, check_me=True):
        if check_me:
            for method in self.methods:
                if method.name == name and len(method.params) == params_count and method.return_type == return_type:
                    return True
        if self.parent:
            return self.parent.get_method(name, params_count, return_type)
        
        return False
    
    def get_params(self):
        if len(self.params) == 0 and self.parent:
                return self.parent.get_params()
        return self.params
    
    def conformed_by(self, name:str) -> bool:
        if self.name == name:
            return True
        elif self.parent:
            return self.parent.conformed_by(name)
        else:
            return False    
    
    def implements(self, protocol:Protocol):
        for method in protocol.methods:
            if not self.get_method(method.name, len(method.params), method.return_type):
                return False
        return True
    
    def __str__(self):
        return f'{self.name}{(" inherits " + self.parent.name) if self.parent else ""} {self.attributes} {self.methods}'
    
    def __rep__(self):
        return self.__str__()