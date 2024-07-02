class ShiftReduceParser:
    SHIFT = 'SHIFT'
    REDUCE = 'REDUCE'
    OK = 'OK'

    def __init__(self, G, verbose=False):
        self.G = G
        self.verbose = verbose
        self.action = {}
        self.goto = {}
        self._build_parsing_table()

    def _build_parsing_table(self):
        raise NotImplementedError()

    def __call__(self, w):
        stack = [0]
        cursor = 0
        output = []
        operations = []
        while True:
            state = stack[-1]
            lookahead = w[cursor]
            if self.verbose: print(stack, '<---||--->', w[cursor:], output)

            if (state, lookahead) not in self.action:
                print("Error")
                print(state, lookahead)
                return None, None

            action, tag = self.action[state, lookahead]
            
            if action == ShiftReduceParser.SHIFT:
                operations.append(ShiftReduceParser.SHIFT)
                stack.append(tag)
                cursor += 1

            elif action == ShiftReduceParser.REDUCE:
                operations.append(ShiftReduceParser.REDUCE)
                for i in range(len(tag.Right)):
                    stack.pop()
                stack.append(self.goto[stack[-1], tag.Left])
                output.append(tag)

            elif action == ShiftReduceParser.OK:
                return output, operations

            else:
                raise ValueError
