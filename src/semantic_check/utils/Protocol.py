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

    def get_method(self, name, params_count, return_type, check_me=True, function = None) -> tuple[bool, bool, bool]:
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
    
    def conformed_by(self, protocol: 'Protocol') -> bool:
        if self.name == protocol.name:
            return True
        elif self.parent:
            return self.parent.conformed_by(protocol)
        else:
            return False    

    def match(self, type) -> bool:
        if isinstance(type, Protocol):
            return self.conformed_by(type)
        else:
            return False

    def __str__(self):
        return f'{self.name}{(" extends " + self.parent.name) if self.parent else ""} {self.methods}'
    
    def __rep__(self):
        return self.__str__()