from utils import DisjointSet, ContainerSet
from automata import DFA


def distinguish_states(group, automaton, partition):
    split = {}
    vocabulary = tuple(automaton.vocabulary)

    transitions = automaton.transitions

    for member in group:
        for aux_group in split.keys():
            for symbol in vocabulary:
                aux_group_p = None
                member_p = None
                try:
                    aux_group_p = partition[transitions[aux_group][symbol][0]].representative
                except KeyError:
                    aux_group_p = None
                try:
                    member_p = partition[transitions[member.value][symbol][0]].representative
                except KeyError:
                    member_p = None
                if not aux_group_p == member_p:
                    break
            else:
                split[aux_group] += [member.value]
                break
        else:
            split[member.value] = [member.value]

    return [group for group in split.values()]


def state_minimization(automaton):
    partition = DisjointSet(*range(automaton.states))

    # partition = { NON-FINALS | FINALS }
    finals = list(automaton.finals)
    non_finals = [state for state in range(automaton.states) if state not in automaton.finals]

    partition.merge(finals)
    partition.merge(non_finals)

    while True:
        new_partition = DisjointSet(*range(automaton.states))

        # Split each group if needed
        for group in partition.groups:
            new_groups = distinguish_states(group, automaton, partition)
            for new_group in new_groups:
                new_partition.merge(new_group)

        if len(new_partition) == len(partition):
            break

        partition = new_partition

    return partition


def automata_minimization(automaton):
    partition = state_minimization(automaton)

    states = [s for s in partition.representatives]

    transitions = {}
    for i, state in enumerate(states):
        origin = state.value

        for symbol, destinations in automaton.transitions[origin].items():
            new_dest = states.index(partition[destinations[0]].representative)

            try:
                transitions[i, symbol]
                assert False
            except KeyError:
                transitions[i, symbol] = new_dest
                pass

    start = states.index(partition[automaton.start].representative)
    finals = set([states.index(partition[final].representative) for final in automaton.finals])

    return DFA(len(states), finals, transitions, start)


def move(automaton, states, symbol):
    moves = set()
    for state in states:
        try:
            moves.update(automaton.transitions[state][symbol])
        except KeyError:
            pass
    return moves


def epsilon_closure(automaton, states):
    pending = list(states)
    closure = set(states)

    while pending:
        state = pending.pop()
        try:
            e_transition = automaton.epsilon_transitions(state)
            pending += e_transition
            closure.update(e_transition)
        except KeyError:
            pass
    return ContainerSet(*closure)


def nfa_to_dfa(automaton):
    transitions = {}

    start = epsilon_closure(automaton, [automaton.start])
    start.id = 0
    start.is_final = any(s in automaton.finals for s in start)
    states = [start]

    pending = [start]
    while pending:
        state = pending.pop()
        for symbol in automaton.vocabulary:
            new_state = move(automaton, state, symbol)
            new_state = epsilon_closure(automaton, new_state)

            if new_state:
                for st in states:
                    if st == new_state:
                        new_state = st
                        break
                else:
                    new_state.id = len(states)
                    new_state.is_final = any(s in automaton.finals for s in new_state)
                    pending.append(new_state)
                    states.append(new_state)
            else:
                continue

            try:
                transitions[state.id, symbol]
                assert False, 'Invalid DFA!!!'
            except KeyError:
                transitions[state.id, symbol] = new_state.id
                pass

    finals = [state.id for state in states if state.is_final]
    dfa = DFA(len(states), finals, transitions)
    return dfa
