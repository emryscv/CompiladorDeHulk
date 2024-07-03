class HULK_error:
    def __init__(self, message, type):
        self.message = message
        self.type = type

    def __str__(self):
        return f"Error: {self.message} \nType: {self.type}"
    
class Argument_is_required(HULK_error):
    def __init__(self):
        super().__init__(f"One argument is required", "Missing Argument")

class Invalid_file_extension(HULK_error):
    def __init__(self):
        super().__init__(f"File must be a .hulk file", "Invalid File")

class Cannot_open_file(HULK_error):
    def __init__(self):
        super().__init__(f"Cannot open file", "File Error")

class TokenNotRecognized(HULK_error):
    def __init__(self, token, row, column):
        super().__init__(f"Token {token} not recognized in Line: {row}, Column: {column}", "Lexer Error")

class UnexspectedSequenceTokens(HULK_error):
    def __init__(self, token, prev_token):
        super().__init__(f"Unexpected token: {token.lex} in Line: {token.row}, Column: {token.column} after {prev_token.lex}", "Parsing Error")