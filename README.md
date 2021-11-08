**A Lambda Calculus Reduction Engine**\
*Reed CSCI 384 : HW 06*

**Description** : A simple parser and reducer for lambda calculus terms.

**Execution** : Run *main.py* with a .lc file name as an argument. To reduce in "verbose" mode, include an optional second argument *True*. Reduction is done in "quiet" mode by default.

**Breakdown**

*main.py* handles overhead to put together the parser and reducer. It reads from a .lc file and hands the text to a parser; receives the parsed terms and hands them to the reducer; and then receives a single reduced term and executes it.

*parser.py* receives a raw lc string and parses it into a list-tree of terms.

*reducer.py* receives a list-tree of lc terms and reduces them to a simplified lc term.

**Bug Notes**

...

**Authors** : Alan Jessup
