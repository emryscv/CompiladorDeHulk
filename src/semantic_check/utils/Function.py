class Function:
    def __init__(self, name, params, return_type):
        self.name = name
        self.params = params
        self.return_type = return_type
        
    def __str__(self):
        return f'{self.name}({self.params}) -> {self.return_type}'