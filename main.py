# Handles overhead to put together the parser and reducer:
# - reads from a lc file and hands the text to a parser,
# - receives the parsed terms as a list-tree and hands them to the reducer, then
# - receives a single reduced lc term.

from lcparser import Parser
from lcreducer import Reducer
import sys

lcfile = sys.argv[1]
verbosemode = False
if len(sys.argv) > 2:
    verbosemode = sys.argv[2].lower() == 'true'

with open(lcfile, 'r') as f:
    lines = f.readlines()
    lctxt = ''
    for line in lines:
        lctxt += line.replace('\n', ' ')

p = Parser(lctxt)
tree = p.get_parsed()
r = Reducer(tree, verbosemode)
term = r.get_reduced_lc()

print(term)
