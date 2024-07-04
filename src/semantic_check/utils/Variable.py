class Variable:
    def __init__(self, name, vtype):
        self.name = name
        self.type = vtype
        
    def __str__(self):
        return f'{self.name}:{self.type}'
    
    def __repr__(self) -> str:
        return self.__str__()