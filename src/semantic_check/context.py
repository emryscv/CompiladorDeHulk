from semantic_check.utils.Type import Type

class Context:
    def __init__(self):
        self.types = {}

    def create_type(self, name:str):
        if name in self.types:
            return [f'Type with the same name ({name}) already in context.']   
        self.types[name] = Type(name)
        return []
        
    def get_type(self, name:str):
        try:
            return self.types[name]
        except KeyError:
              
            return (f'Type "{name}" is not defined.') #arreglar esta historia

    def __str__(self):
        return '{\n\t' + '\n\t'.join(str(x) for x in self.types.values()) + '\n}'

    def __repr__(self):
        return str(self)