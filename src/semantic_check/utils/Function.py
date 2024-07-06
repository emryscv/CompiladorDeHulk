class Function:
    def __init__(self, name, params, return_type, body):
        self.name = name
        self.params = params
        self.return_type = return_type
        self.body= body
        
    def __str__(self):
        return f'{self.name}({self.params}) -> {self.return_type}'
    
    def __repr__(self) -> str:
        return self.__str__()