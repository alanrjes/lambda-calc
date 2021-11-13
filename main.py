# Handles overhead to put together the parser and reducer:
# - reads from a .lc file and hands the text to a parser,
# - receives the parsed terms and hands them to the reducer, then
# - receives a single reduced term and executes.

from lcparser import Parser
#from lcreducer import Reducer
import sys

lcfile = sys.argv[1]
if len(sys.argv) > 2:
    verbosemode = sys.argv[2] == 'True'

with open(lcfile, 'r') as f:
    lines = f.readlines()
    lctxt = ''
    for line in lines:
        lctxt += line.replace('\n', ' ')

p = Parser(lctxt)
tree = p.get_parsed()
print(tree)
#r = Reducer(tree)
#term = r.get_reduced()

#print(term)
