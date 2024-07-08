from semantic_check.utils.Function import Function
from semantic_check.utils.Variable import Variable
from semantic_check.utils.Protocol import Protocol

class Type:
    def __init__(self, name:str):
        self.name = name
        self.attributes: list[Variable] = []
        self.methods: list[Function] = []
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
    
    def get_method(self, name, params_count, return_type, check_me=True) -> tuple[bool, bool, bool]:
        name_match = name_match_parent = False
        params_match = params_match_parent = False
        return_match = return_match_parent = False
        function = function_parent = None
        
        if check_me:
            for method in self.methods:
                if method.name == name:
                    if not name_match:
                        name_match = True
                        function = method
                    if len(method.params) == params_count:
                        if not params_match:
                            params_match = True
                            function = method
                        if method.return_type == return_type:
                            return_match = True
                            return (name_match, params_match, return_match, method)
        
        if self.parent: 
            name_match_parent, params_match_parent, return_match_parent, function_parent = self.parent.get_method(name, params_count, return_type)
        
        if (not name_match and name_match_parent) or (not params_match and params_match_parent) or (not return_match and return_match_parent):
            return (name_match_parent, params_match_parent, return_match_parent, function_parent)
        else:
            return (name_match, params_match, return_match, function)
        
    
    def get_params(self):
        if len(self.params) == 0 and self.parent:
                return self.parent.get_params()
        return self.params
    
    def conformed_by(self, type: 'Type') -> bool:
        if self.name == type.name:
            return True
        elif self.parent:
            return self.parent.conformed_by(type)
        else:
            return False    
    
    def implements(self, protocol:Protocol):
        for method in protocol.methods:
            name_match, params_match, return_match, function = self.get_method(method.name, len(method.params), method.return_type)
            if (name_match, params_match, return_match) != (True, True, True):
                return False
        return True
    
    def match(self, type) -> bool: #TODO ver porq no se pued eponer Type aqui
        if isinstance(type, Type):
            return self.conformed_by(type)
        else:
            return self.implements(type)    
    
    def __str__(self):
        return f'{self.name}{(" inherits " + self.parent.name) if self.parent else ""} {self.attributes} {self.methods}'
    
    def __rep__(self):
        return self.__str__()
    