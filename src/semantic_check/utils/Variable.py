class Variable:
    def __init__(self, name, vtype):
        self.name = name
        self.vtype = vtype
        
    def __str__(self):
        return f'{self.name}:{self.vtype}'
    
    def __repr__(self) -> str:
        return self.__str__()