# Receives a list-tree of lc terms and reduces them to a simplified lc term.

import string

def gen_vars():  # gives a list of 260 unique 2-character variable names to use for substitution
    l = []
    for c1 in string.ascii_lowercase:
        for c2 in range(0, 10):
            l.append(c1+str(c2))
    return l

class Reducer:
    def __init__(self, tree, verbosemode):
        self.verbosemode = verbosemode
        self.varnames = gen_vars()
        self.stree = []
        for branch in tree:  # get substituted version of the tree w/ unique vars
            self.stree.append(self.substitute(branch))
        #...
        #self.reduce_full()

    def vprint(self, t):
        if self.verbosemode:
            print(t)

    def substitute(self, term, lvars={}):
        if term[0] == 'LM':
            v = term[1]
            vp = self.varnames.pop(0)
            lvars[v] = vp
            e = self.substitute(term[2], lvars)
            return ['LM', vp, e]
        elif term[0] == 'VA':
            v = term[1]
            if v in lvars:
                vp = lvars[v]
            else:
                vp = self.varnames.pop(0)
                lvars[v] = vp
            return ['VA', vp]
        elif term[0] == 'AP':
            e1 = self.substitute(term[1], lvars)
            e2 = self.substitute(term[2], lvars)
            return ['AP', e1, e2]
        else:
            print(term)

    def reduce_term(self, term):
        pass

    def reduce_full(self):
        pass

    def get_reduced(self):
        return self.redterm
