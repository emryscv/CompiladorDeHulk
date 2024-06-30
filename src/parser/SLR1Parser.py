from parser.SRParser import ShiftReduceParser
from parser.parsing_utils import build_LR0_automaton, compute_firsts, compute_follows


class SLR1Parser(ShiftReduceParser):
    def _build_parsing_table(self):
        G = self.G.AugmentedGrammar(True)
        firsts = compute_firsts(G)
        follows = compute_follows(G, firsts)

        automaton = build_LR0_automaton(G).to_deterministic()
        for i, node in enumerate(automaton):
            if self.verbose: print(i, '\t', '\n\t '.join(str(x) for x in node.state), '\n')
            node.idx = i

        for node in automaton:
            idx = node.idx
            for state in node.state:
                item = state.state

                if item.IsReduceItem:
                    if item.production.Left == G.startSymbol:
                        self._register(self.action, (idx, G.EOF), (SLR1Parser.OK, None))
                    else:
                        for symbol in follows[item.production.Left]:
                            self._register(self.action, (idx, symbol), (SLR1Parser.REDUCE, item.production))
                else:
                    next_symbol = item.NextSymbol
                    key = (idx, next_symbol)
                    next_idx = node.transitions[next_symbol.Name][0].idx

                    if next_symbol.IsTerminal:
                        self._register(self.action, key, (SLR1Parser.SHIFT, next_idx))
                    else:
                        self._register(self.goto, key, next_idx)

    @staticmethod
    def _register(table, key, value):
        assert key not in table or table[key] == value, 'Shift-Reduce or Reduce-Reduce conflict!!!'
        table[key] = value
