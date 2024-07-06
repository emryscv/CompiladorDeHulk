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
            "Iterable": Type("Iterable") #TODO añadirle los metodos q hacen falta
        }
        
        object = self.get_type("Object")
        self.get_type("String").parent = object
        self.get_type("Number").parent = object
        self.get_type("Boolean").parent = object

    def create_type(self, name:str):
        message = self.is_defined(name)
        
        if len(message) == 0:
            self.types[name] = Type(name)
        
        return message
    
    def create_protocol(self, name:str):
        message = self.is_defined(name)
        
        if len(message) == 0:
            self.types[name] = Protocol(name)
        
        return message
        
    def is_type_defined(self, name:str):
        if name in self.types:
            return []
        
        return (f'Type "{name}" is not defined.')
    
    def is_protocol_defined(self, name:str):
        if name in self.protocols:
            return []
        
        return (f'Protocol "{name}" is not defined.')
    
    def is_defined(self, name:str):
        if name in self.types:
            return [f'Type with the same name ({name}) already in context.']
        
        if name in self.protocols:
            return [f'Protocol with the same name ({name}) already in context.']
        
        return []
    
    def get_type(self, name:str):
        return self.types[name]
    
    def get_protocol(self, name:str):
        return self.types[name]
    
    
    def __str__(self):
        return '{\n\t' + '\n\t'.join(str(x) for x in self.types.values()) + '\n}'

    def __repr__(self):
        return str(self)