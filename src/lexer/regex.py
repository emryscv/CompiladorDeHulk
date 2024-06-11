from src.grammars.regex_grammar import get_regex_grammar
from src.parser.SLR1Parser import SLR1Parser
from src.parser.parsing_utils import evaluate_reverse_parse
from src.lexer.build_regex_automata import RegexAutomataBuilder
from src.utils.automata_utils import nfa_to_dfa, automata_minimization
from src.utils.utils import Token


class Regex:
    def __init__(self, regex):
        self.G = get_regex_grammar()
        self.parser = SLR1Parser(self.G)
        self.regex = regex
        self.dfa, self.errors = self.build_regex(self.regex)

    def build_regex(self, regex):
        tokens = []
        errors = []

        for i, c in enumerate(regex):

            token = [x for x in self.G.terminals if x.Name == c]
            if len(token) > 0:
                tokens.append(token[0])
            else:
                errors.append(f"Invalid character {c} on column {i}")

        tokens.append(self.G.EOF)
        derivation, operations = self.parser(tokens)
        tokens = [Token(x.Name, x, 0) for x in tokens]
        ast = evaluate_reverse_parse(derivation, operations, tokens)
        evaluator = RegexAutomataBuilder()

        nfa = evaluator.visit(ast)
        dfa = nfa_to_dfa(nfa)
        dfa = automata_minimization(dfa)
        return dfa, errors
