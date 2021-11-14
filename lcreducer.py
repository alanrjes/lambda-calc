# Receives a list-tree of lc terms and reduces them, then translates back to lc and returns a simplified lc term.

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
        self.varkeys = {'main':'main'}
        self.rtree = []
        for branch in tree:  # get renamed version of the tree w/ unique vars
            rbranch = self.rename(branch)
            self.rtree.append(rbranch)
        self.redterm = self.reduce()  # substitute & evaluate; normal-order beta reduction

    def vprint(self, v, a):
        if self.verbosemode:
            vp = self.varkeys[v]
            ap = self.restore(a)
            print('Evaluated lambda '+vp+' with arg '+ap+' to get:')

    def rename(self, term, lvars={}):  # alpha-renaming step
        if term[0] in ['LM', 'EQ']:
            v = term[1]
            if v == 'main':  # preserve 'main' var name
                vp = 'main'
            else:
                vp = self.varnames.pop(0)
                self.varkeys[vp] = v  # save key to change back at the end
                lvars[v] = vp
            e = self.rename(term[2], lvars)
            return ['LM', vp, e]
        elif term[0] == 'VA':
            v = term[1]
            if v in lvars:
                vp = lvars[v]
            else:
                vp = self.varnames.pop(0)
                self.varkeys[vp] = v
                lvars[v] = vp
            return ['VA', vp]
        elif term[0] == 'AP':
            e1 = self.rename(term[1], lvars)
            e2 = self.rename(term[2], lvars)
            return ['AP', e1, e2]

    def sub_eqs(self, term, gvars):  # substitute ":="-level variables
        if term[0] == 'LM':
            e = term[2]
            ep = self.sub_eqs(e, gvars)
            return ['LM', term[1], ep]
        elif term[0] == 'VA':
            v = term[1]
            if v in gvars:
                sv = gvars[v]
                return self.sub_eqs(sv, gvars)
            else:
                return term
        elif term[0] == 'AP':
            e1 = term[1]
            e2 = term[2]
            ep1 = self.sub_eqs(e1, gvars)
            ep2 = self.sub_eqs(e2, gvars)
            return ['AP', ep1, ep2]

    def eval_lms(self, term):  # substitute/evaluate lambdas using normal order reduction
        if term[0] == 'AP':
            if term[1][0] == 'LM':
                v = term[1][1]  # eg. AP[LM(x, (x y)), VA(y)] -> (y y), where v=x, arg=y, fun=(x y)
                arg = term[2]
                fun = term[1][2]
                self.vprint(v, arg)
                return self.eval_sub(fun, v, arg), True  # bool flag to indicate a reduction was made
            else:
                ep1, f1 = self.eval_lms(term[1])
                ep2, f2 = self.eval_lms(term[2])
                return ['AP', ep1, ep2], (f1 or f2)
        elif term[0] == 'VA':
            return term, False  # recursion base case
        elif term[0] == 'LM':
            v = term[1]
            e = term[2]
            ep, f = self.eval_lms(e)
            return ['LM', v, ep], f

    def eval_sub(self, term, v, e):  # replaces all occurances of v in the term with e
        if term[0] == 'LM':
            ep = self.eval_sub(term[2], v, e)
            return ['LM', term[1], ep]
        elif term[0] == 'VA':
            if term[1] == v:
                return e
            else:
                return term
        elif term[0] == 'AP':
            ep1 = self.eval_sub(term[1], v, e)
            ep2 = self.eval_sub(term[2], v, e)
            return ['AP', ep1, ep2]

    def reduce(self):
        gvars = {}
        for branch in self.rtree:  # all EQ terms (lines)
            v = branch[1]
            e = branch[2]
            gvars[v] = e
        main = self.sub_eqs(gvars['main'], gvars)
        if self.verbosemode:
            lmmain = self.restore(main)
            print('Substituted to:\n'+lmmain+'\n')
        flag = True
        while flag:
            main, flag = self.eval_lms(main)
            if self.verbosemode:
                lmmain = self.restore(main)
                print(lmmain+'\n')
        return main

    def restore(self, term):
        if term[0] == 'LM':
            v = term[1]
            e = term[2]
            vp = self.varkeys[v]
            es = self.restore(e)
            return 'fn '+vp+' => '+es
        elif term[0] == 'VA':
            v = term[1]
            vp = self.varkeys[v]
            return vp
        elif term[0] == 'AP':
            e1 = term[1]
            e2 = term[2]
            es1 = self.restore(e1)
            es2 = self.restore(e2)
            return '('+es1+' '+es2+')'

    def get_reduced_lc(self):  # translates the reduced term back into lc syntax and restores variable names
        term = self.redterm
        lc = self.restore(term)
        return lc
