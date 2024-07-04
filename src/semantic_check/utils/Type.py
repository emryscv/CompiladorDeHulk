class Type:
    def __init__(self, name:str):
        self.name = name
        self.attributes = []
        self.methods = []
        self.parent = None
        
    def __str__(self):
        return f'{self.name} inherits {self.parent}'