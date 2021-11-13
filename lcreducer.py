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
        self.rtree = []
        for branch in tree:  # get renamed version of the tree w/ unique vars
            self.rtree.append(self.rename(branch))
        self.rlib = {}
        self.redterm = self.reduce()

    def vprint(self, t):
        if self.verbosemode:
            print(t)

    def rename(self, term, lvars={}):  # alpha-renaming step
        if term[0] == 'LM':
            v = term[1]
            if v == 'main':  # preserve 'main' var name
                vp = 'main'
            else:
                vp = self.varnames.pop(0)
                lvars[v] = vp
            e = self.rename(term[2], lvars)
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
            e1 = self.rename(term[1], lvars)
            e2 = self.rename(term[2], lvars)
            return ['AP', e1, e2]

    def substitute(self, term):  # substitution step of beta-reduction
        if term[0] == 'LM':
            v = term[1]
            e = self.substitute(term[2])
            self.rlib[v] = e
            return ['LM', v, e]
        elif term[0] == 'VA':
            v = term[1]
            if v in self.rlib:
                return self.rlib[v]
            else:
                return term  # recursion base case
        elif term[0] == 'AP':
            e1 = self.substitute(term[1])
            e2 = self.substitute(term[2])
            return ['AP', e1, e2]

    def eval_sub(self, term, v, e=None):  # replaces all v in term with e to evaluate and LM
        if term[0] == 'LM':
            ep = self.eval_sub(term[2], v, e)
            return ['LM', term[1], ep]
        elif term[0] == 'VA':
            if term[1] == v:
                if e:
                    return e
                else:
                    raise ValueError()
            else:
                return term
        elif term[0] == 'AP':
            ep1 = self.eval_sub(term[1], v, e)
            ep2 = self.eval_sub(term[2], v, e)
            return ['AP', ep1, ep2]

    def evaluate(self, term):  # normal order evaluation step of beta-reduction
        if term[0] == 'AP':
            if term[1][0] == 'LM':
                v = term[1][1]  # eg. AP[LM(x, (x y)), VA(y)] -> (y y), where v=x, e=y, t = (x y)
                einpt = term[2]
                eenv = term[1][2]
                return self.eval_sub(eenv, v, einpt)
            else:
                ep1 = self.evaluate(term[1])
                ep2 = self.evaluate(term[2])
                return ['AP', ep1, ep2]
        elif term[0] == 'VA':
            return term  # recursion base case
        elif term[0] == 'LM':
            v = term[1]
            e = term[2]
            try:
                return self.eval_sub(e, v)  # try to evaluate with no e to see if it's not needed
            except ValueError:  # outer lamda can't be reduced, so reduce next
                return ['LM', v, self.evaluate(e)]

    def reduce(self):
        self.vprint('Renamed form: '+str(self.rtree))
        for rbranch in self.rtree:
            sbranch = self.substitute(rbranch)
        subdterm =  self.rlib['main']
        self.vprint('Substituted form: '+str(subdterm))
        t1 = []
        t2 = subdterm
        while t1 != t2:
            t1 = t2
            t2 = self.evaluate(t2)
        return t2

    def get_reduced(self):
        return self.redterm
