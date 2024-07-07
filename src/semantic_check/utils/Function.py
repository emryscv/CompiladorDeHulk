class Function:
    def __init__(self, name, params, return_type, body=None, is_method=False):
        self.name = name
        self.params = params
        self.return_type = return_type
        self.body= body
        self.is_method = is_method
        
    def __str__(self):
        return f'{self.name}({self.params}) -> {self.return_type}'
    
    def __repr__(self) -> str:
        return self.__str__()