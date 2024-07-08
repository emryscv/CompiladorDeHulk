from semantic_check.utils.Type import Type
from semantic_check.utils.Protocol import Protocol

class Context:
    def __init__(self):
        self.types: dict[str, Type]= {
            "Object": Type("Object"), 
            "String": Type("String"),
            "Number": Type("Number"),
            "Boolean": Type("Boolean"),
            "Range": Type("Range")
        }
        self.protocols: dict[str, Protocol] = {
            "Iterable": Protocol("Iterable")
        }
                
        object = self.get_type("Object")[1]
        self.get_type("String")[1].parent = object
        self.get_type("Number")[1].parent = object
        self.get_type("Boolean")[1].parent = object
        
        range_type = self.get_type("Range")[1]
        range_type.parent = object
        range_type.params = [("min", "Number"), ("max", "Number")]
        range_type.define_attribute("min", "Number")
        range_type.define_attribute("max", "Number")
        range_type.define_attribute("current", "Number")
        range_type.define_method("next", [], "Boolean")
        range_type.define_method("current", [], "Number")
        
        iterable = self.get_protocol("Iterable")[1]
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
        if self.is_type_defined(name):
            return (True, self.types[name])

        return (False, self.types["Object"])
        
    def get_protocol(self, name:str):
        if self.is_protocol_defined(name):
            return (True, self.protocols[name])
        
        return (False, None) #TODO un protocolo base
    
    def get(self, name: str):
        if self.is_type_defined(name):
            return self.get_type(name)
        if self.is_protocol_defined(name):
            return self.get_protocol(name)
        
        return (False, self.types["Object"])
    
    def __str__(self):
        return '{\n\ttypes:{\n\t\t' + '\n\t\t'.join(str(x) for x in self.types.values()) + '\n\t}\n\tprotoocols:{\n\t\t' + '\n\t\t'.join(str(x) for x in self.protocols.values()) + '\n\t}\n}'

    def __repr__(self):
        return str(self)