from  utils.utils import Token
from  lexer.regex import Regex
from  utils.automata import State


class Lexer:
    def __init__(self, table, eof):
        self.eof = eof
        self.regexs = self._build_regexs(table)
        self.automaton = self._build_automaton()

    def _build_regexs(self, table):
        regexs = []
        for n, (token_type, regex) in enumerate(table):
            a = Regex(regex).dfa
            state, other_states = State.from_nfa(a, get_states=True)
            for st in other_states:
                if st.final:
                    st.tag = (n, token_type)
            regexs.append(state)
        return regexs

    def _build_automaton(self):
        start = State('start')
        for automaton in self.regexs:
            start.add_epsilon_transition(automaton)
        return start.to_deterministic()

    def _walk(self, string):
        state = self.automaton
        final = state if state.final else None
        final_lex = lex = ''

        for symbol in string:
            lex += symbol
            try:
                state = state.get(symbol)
                if state.final:
                    final = state
                    final_lex = lex
            except KeyError:
                break

        return final, final_lex

    def _tokenize(self, text):
        row = column = 1
        while text:
            print(text[0])
            match text[0]:
                case '\n':
                    row += 1
                    column = 0

            final_state, lex = self._walk(text)

            assert len(lex) != 0, 'Error'

            priority = [state.tag for state in final_state.state if state.tag]
            priority.sort()
            idx, token_type = priority[0]

            text = text[len(lex):]
            yield lex, token_type, row, column

            column += len(lex)

        yield '$', self.eof, row, column

    def __call__(self, text):
        return [Token(lex, ttype, row, column) for lex, ttype, row, column in self._tokenize(text) if not ttype == 'space']