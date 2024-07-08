from typing import Union

class Variable:
    def __init__(self, name:str, vtype, value=None):
        self.name = name
        self.vtype = vtype
        self.value = value
        
    def __str__(self):
        return f'{self.name}:{self.vtype}'
    
    def __repr__(self) -> str:
        return self.__str__()