class HULK_error:
    def __init__(self, message, type):
        self.message = message
        self.type = type

    def __str__(self):
        return f"Error: {self.message}. Type: {self.type}"
    
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
        super().__init__(f"Unexpected token: {token.lex} in Line: {token.row}, Column: {token.column} after {prev_token.lex}", "Semantic Error")

class Invalid_Type(HULK_error):
    def __init__(self, type, row, column):
        super().__init__(f'Type "{type}" is not defined in Line: {row}, Column: {column}', "Semantic Error")
        

class   Invalid_Argument_Type(HULK_error):
    def __init__(self, position, function_id, param_type, arg_type, row, column):
        super().__init__(f'Argument number: {position} in ({function_id}) has type ({param_type}) but ({arg_type}) was given  in Line: {row}, Column: {column}', "Semantic Error")

class Invalid_Initialize_type(HULK_error):
    def __init__(self, variable_id, vtype, expr_type, row, column):
        super().__init__(f'Variable: ({variable_id}) has type {vtype} and {expr_type} was given in Line: {row}, Column: {column}', "Semantic Error")
        
class Invalid_Operation(HULK_error):
    def __init__(self, operator, left_type, right_type, row, column):
        super().__init__(f'Operator: ({operator}) can\'t be applied to {left_type} and {right_type} in Line: {row}, Column: {column}', "Semantic Error")

class Self_Not_Target(HULK_error):
     def __init__(self, row, column):
        super().__init__(f'`self` is not a valid assignment target in Line: {row}, Column: {column}', "Semantic Error")

class Boolean_Expected(HULK_error):
    def __init__(self, condition_type, row, column):
        super().__init__(f'Boolean expression expected but {condition_type} was given in Line: {row}, Column: {column}', "Semantic Error")

class Invalid_Arg_Count(HULK_error):    
    def __init__(self, function_id, params_count, arg_count, row, column):
        super().__init__(f'{function_id} expects {params_count} params but {arg_count}was given in Line: {row}, Column: {column}', "Semantic Error")
