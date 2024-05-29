from automata import NFA


def automata_closure(a1):
    transitions = {}

    start = 0
    d1 = 1
    final = a1.states + d1

    for (origin, symbol), destinations in a1.map.items():
        transitions[origin + d1, symbol] = [dest + d1 for dest in destinations]

    transitions[start, ''] = [a1.start + d1, final]

    for f1 in a1.finals:
        transitions[f1 + d1, ''] = [final, a1.start + d1]

    states = a1.states + 2
    finals = {final}

    return NFA(states, finals, transitions, start)


def automata_union(automata_1, automata_2):
    transitions = {}

    start = 0
    d1 = 1
    d2 = automata_1.states + d1
    final = automata_2.states + d2

    for (origin, symbol), destinations in automata_1.map.items():
        transitions[d1 + origin, symbol] = [dest + d1 for dest in destinations]

    for (origin, symbol), destinations in automata_2.map.items():
        transitions[d2 + origin, symbol] = [dest + d2 for dest in destinations]

    transitions[start, ''] = [automata_1.start + d1, automata_2.start + d2]

    for f1, f2 in zip(automata_1.finals, automata_2.finals):
        transitions[f1 + d1, ''] = [final]
        transitions[f2 + d2, ''] = [final]

    states = automata_1.states + automata_2.states + 2
    finals = {final}
    return NFA(states, finals, transitions, start)


def automata_concatenation(automata_1, automata_2):
    transitions = {}

    start = 0
    d1 = 0
    d2 = automata_1.states + d1
    final = automata_2.states + d2

    for (origin, symbol), destinations in automata_1.map.items():
        transitions[origin + d1, symbol] = [dest + d1 for dest in destinations]

    for (origin, symbol), destinations in automata_2.map.items():
        transitions[origin + d2, symbol] = [dest + d2 for dest in destinations]

    for f1 in automata_1.finals:
        transitions[f1 + d1, ''] = [automata_2.start + d2]

    for f2 in automata_2.finals:
        transitions[f2 + d2, ''] = [final]

    states = automata_1.states + automata_2.states + 1
    finals = {final}

    return NFA(states, finals, transitions, start)


def automata_symbol(lex):
    return NFA(2, [1], {(0, lex): [1], })
