from semantic_check.utils.Type import Type

class Context:
    def __init__(self):
        self.types = {
            "Object" : Type("Object"), 
            "String": Type("String"),
            "Number": Type("Number"),
            "Boolean": Type("Boolean"),
        }
        self.protocols = {
            
        }
        
        object = self.get_type("Object")
        self.get_type("String").parent = object
        self.get_type("Number").parent = object
        self.get_type("Boolean").parent = object

    def create_type(self, name:str):
        if name in self.types:
            return [f'Type with the same name ({name}) already in context.']   
        self.types[name] = Type(name)
        return []
        
    def is_type_defined(self, name:str):
        if name in self.types:
            return []
        
        return (f'Type "{name}" is not defined.')
    
    def get_type(self, name:str):
        return self.types[name]
    
    def create_protocol(self, name:str):
        if name in self.protocols:
            return [f'Protocol with the same name ({name}) already in context.']   
        self.types[name] = Type(name)
        return []
        
    def is_protocol_defined(self, name:str):
        if name in self.types:
            return []
        
        return (f'Type "{name}" is not defined.')
    
    def get_protocol(self, name:str):
        return self.types[name]
    
    
    def __str__(self):
        return '{\n\t' + '\n\t'.join(str(x) for x in self.types.values()) + '\n}'

    def __repr__(self):
        return str(self)