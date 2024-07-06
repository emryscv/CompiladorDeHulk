from semantic_check.utils.Type import Type
from semantic_check.utils.Protocol import Protocol

class Context:
    def __init__(self):
        self.types: dict[str, Type]= {
            "Object": Type("Object"), 
            "String": Type("String"),
            "Number": Type("Number"),
            "Boolean": Type("Boolean"),
        }
        self.protocols: dict[str, Protocol] = {
            "Iterable": Protocol("Iterable")
        }
                
        object = self.get_type("Object")
        self.get_type("String").parent = object
        self.get_type("Number").parent = object
        self.get_type("Boolean").parent = object

        iterable = self.get_protocol("Iterable")
        iterable.declare_method("next", [], "Boolean")
        iterable.declare_method("current", [], "Object")

    def create_type(self, name:str):
        self.types[name] = Type(name)
    
    def create_protocol(self, name:str):
        self.protocols[name] = Protocol(name)
                
    def is_type_defined(self, name:str):
        if name in self.types:
            return True
        
        return False
    
    def is_protocol_defined(self, name:str):
        if name in self.protocols:
            return True
        
        return False
    
    def get_type(self, name:str):
        return self.types[name]
    
    def get_protocol(self, name:str):
        return self.protocols[name]
    
    def __str__(self):
        return '{\n\ttypes:{\n\t\t' + '\n\t\t'.join(str(x) for x in self.types.values()) + '\n\t}\n\tprotoocols:{\n\t\t' + '\n\t\t'.join(str(x) for x in self.protocols.values()) + '\n\t}\n}'

    def __repr__(self):
        return str(self)