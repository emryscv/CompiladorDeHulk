import src.utils.visitor as visitor
from src.ast_nodes.regex_nodes import *
from src.utils.automata_operations import *


class RegexAutomataBuilder(object):

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(UnionNode)
    def visit(self, node):
        l_automata = self.visit(node.left)
        r_automata = self.visit(node.right)
        return automata_union(l_automata, r_automata)

    @visitor.when(ConcatNode)
    def visit(self, node):
        l_automata = self.visit(node.lef)
        r_automata = self.visit(node.right)
        return automata_concatenation(l_automata, r_automata)

    @visitor.when(ClosureNode)
    def visit(self, node):
        automata = self.visit(node.node)
        return automata_closure(automata)

    @visitor.when(SymbolNode)
    def visit(self, node):
        return automata_symbol(node.lex)
    