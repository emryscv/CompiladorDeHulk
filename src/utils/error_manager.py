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

class Not_Defined(HULK_error):
    def __init__(self, type, token):
        super().__init__(f'{type} "{token.lex}" is not defined in Line: {token.row}, Column: {token.column}', "Semantic Error")
        
class Not_Defined_In(HULK_error): #TODO pasarle el token
    def __init__(self, type, identifier, name, row, column):
        super().__init__(f'{type} "{identifier}" is not defined in {name} Line: {row}, Column: {column}', "Semantic Error")
        
class Already_Defined(HULK_error):
    def __init__(self, type, identifier):
        super().__init__(f'{type} with the same name ({identifier.lex}) is already defined in Line: {identifier.row}, Column: {identifier.column}', "Semantic Error")
        
class Already_Defined_In(HULK_error):
    def __init__(self, type, identifier, type_name):
        super().__init__(f'{type} with the same name ({identifier.lex}) is already defined in ({type_name}) in Line: {identifier.row}, Column: {identifier.column}', "Semantic Error")
    
class Invalid_Argument_Type(HULK_error):
    def __init__(self, position, function_id, param_type, arg_type, row, column):
        super().__init__(f'Argument number: {position} in ({function_id}) has type ({param_type}) but ({arg_type}) was given  in Line: {row}, Column: {column}', "Semantic Error")

class Invalid_Initialize_type(HULK_error):
    def __init__(self, variable, vtype, expr_type):
        super().__init__(f'Variable: ({variable.lex}) has type {vtype} but {expr_type} was given in Line: {variable.row}, Column: {variable.column}', "Semantic Error")
        
class Invalid_Operation(HULK_error):
    def __init__(self, operator, left_type, right_type):
        super().__init__(f'Operator: ({operator.lex}) can\'t be applied to {left_type} and {right_type} in Line: {operator.row}, Column: {operator.column}', "Semantic Error")

class Self_Not_Target(HULK_error):
     def __init__(self, row, column):
        super().__init__(f'`self` is not a valid assignment target in Line: {row}, Column: {column}', "Semantic Error")

class Boolean_Expected(HULK_error):
    def __init__(self, condition_type, row, column):
        super().__init__(f'Boolean expression expected but {condition_type} was given in Line: {row}, Column: {column}', "Semantic Error")

class Invalid_Arg_Count(HULK_error):    
    def __init__(self, function_id, params_count, arg_count):
        super().__init__(f'{function_id.lex} expects {params_count} params but {arg_count}was given in Line: {function_id.row}, Column: {function_id.column}', "Semantic Error")

class Forbiden_Inheritance(HULK_error):
    def __init__(self, base_identifier):
        if base_identifier.lex in ["Number", "String", "Boolean", "Object"]:
            super().__init__(f'A Type can\'t inherits from {base_identifier.lex} in Line: {base_identifier.row}, Column: {base_identifier.column}', "Semantic Error")
        else:
            super().__init__(f'A Type can\'t inherits from a Protocol in Line: {base_identifier.row}, Column: {base_identifier.column}', "Semantic Error")

class Forbiden_Extends(HULK_error):
    def __init__(self, base_identifier):
        super().__init__(f'A Protocol can\'t extends a Type in Line: {base_identifier.identifier}, Column: {base_identifier.column}', "Semantic Error")