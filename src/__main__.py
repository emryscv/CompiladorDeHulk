import sys
from pathlib import Path

from grammars.HULK_grammar import *
from ast_nodes.hulk_ast_nodes import *
from lexer.lexer_gen import Lexer
from lexer.regex_table import regex_table
from parser.LR1Parser import LR1Parser
from parser.SRParser import ShiftReduceParser
from utils.error_manager import *
from parser.parsing_utils import evaluate_reverse_parse
from semantic_check.FormatVisitor import FormatVisitor

def main(code_path):
    if not Path(code_path).suffix == ".hulk":
        error = Invalid_file_extension()
        print(error)
        sys.exit(1)
    try:
        with open(code_path, 'r') as file:
            code = file.read()
    except:
        error = Cannot_open_file()
        print(error)
        sys.exit(1)
    
    lexer = Lexer(regex_table, G.EOF)
    tokens, lexer_errors = lexer(code)
    if lexer_errors:
        for error in lexer_errors:
            print(error)
        sys.exit(1)

    print(tokens)
    
    parser = LR1Parser(G, verbose=False)
    derivation, operations_or_error = parser(tokens)

    if not derivation:
        print(operations_or_error)
        sys.exit(1) 
        
    ast = evaluate_reverse_parse(derivation, operations_or_error, tokens)

    formatter = FormatVisitor()
    print(formatter.visit(ast))
    
if __name__ == "__main__":
    if not len(sys.argv) == 2:
        error = Argument_is_required()
        print(error)
        sys.exit(1)
    hulk_path = sys.argv[1]
    main(hulk_path)