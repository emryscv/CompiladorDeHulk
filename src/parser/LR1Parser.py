from  parser.parsing_utils import build_LR1_automaton
from  parser.SRParser import ShiftReduceParser

class LR1Parser(ShiftReduceParser):
    def _build_parsing_table(self):
        G = self.G.AugmentedGrammar(True)

        automaton = build_LR1_automaton(G)
        for i, node in enumerate(automaton):
            if self.verbose: print(i, '\t', '\n\t '.join(str(x) for x in node.state), '\n')
            node.idx = i

        for node in automaton:
            idx = node.idx
            for item in node.state:
                if item.IsReduceItem:
                    if item.production.Left == G.startSymbol:
                        self._register(self.action, (idx, G.EOF), (LR1Parser.OK, None))
                    else:
                        for symbol in item.lookaheads:
                            self._register(self.action, (idx, symbol), (LR1Parser.REDUCE, item.production))
                else:
                    next_symbol = item.NextSymbol
                    key = (idx, next_symbol)
                    next_idx = node[next_symbol.Name][0].idx

                    if next_symbol.IsTerminal:
                        self._register(self.action, key, (LR1Parser.SHIFT, next_idx))
                    else:
                        self._register(self.goto, key, next_idx)
                pass

    @staticmethod
    def _register(table, key, value):
        assert key not in table or table[key] == value, 'Shift-Reduce or Reduce-Reduce conflict!!!'
        table[key] = value