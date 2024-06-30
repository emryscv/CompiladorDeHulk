from  grammars.regex_grammar import *
from  parser.SLR1Parser import SLR1Parser
from  parser.parsing_utils import evaluate_reverse_parse
from  lexer.build_regex_automata import RegexAutomataBuilder
from  utils.automata_utils import nfa_to_dfa, automata_minimization
from  utils.utils import Token

fixed_tokens = {
        '|': Token('|', pipe),
        '*': Token('*', star),
        '(': Token('(', opar),
        ')': Token(')', cpar)
    }

class Regex:
    def __init__(self, regex):
        self.parser = SLR1Parser(G, True)
        self.regex = regex
        self.dfa, self.errors = self.build_regex(self.regex)

    def build_regex(self, regex):
        tokens = []
        errors = []

        for i, c in enumerate(regex):
            token = []
            try:
                token.append(fixed_tokens[c])
            except:
                token.append(Token(c, symbol))

            if len(token) > 0:
                tokens.append(token[0])
            else:
                errors.append(f"Invalid character {c} on column {i}")

        tokens.append(Token('$', G.EOF))
        derivation, operations = self.parser([t.token_type for t in tokens])
        ast = evaluate_reverse_parse(derivation, operations, tokens)
        evaluator = RegexAutomataBuilder()

        nfa = evaluator.visit(ast)
        dfa = nfa_to_dfa(nfa)
        dfa = automata_minimization(dfa)
        return dfa, errors
