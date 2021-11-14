**A Lambda Calculus Reduction Engine**\
*Reed CSCI 384 : HW 06*

**Description** : A simple parser and reducer for lambda calculus terms.

**Execution** : Run *main.py* with a .lc file name as an argument. To reduce in "verbose" mode, include an optional second argument *True*. Reduction is done in "quiet" mode by default.

**Breakdown**

*main.py* handles overhead to put together the parser and reducer. It reads from a .lc file and hands the text to a parser; receives the parsed terms and hands them to the reducer; and then receives a single reduced term and executes it.

*parser.py* receives a raw lc string and parses it into a list-tree of terms. The Parser class first separates the raw string of lc text into tokens; then it parses each line by tokens, and stores all lines in a list-tree. This is all done on the creation of a Parser object, and the tree can be accessed with the *get_parsed* method.

*reducer.py* receives a list-tree of lc terms and reduces them to a simplified lc term. The Reducer class first renames all variables using alpha-renaming (limited to 260 variables). Then it reduces the term; first at the line-level with variables defined by ":=", and then using normal-order beta reduction to evaluate lambda terms. If in "verbose" mode, these reduction are printed out. The reduced term can then be translated back into lc with restored variable names, and accessed with the *get_reduced_lc* method.

**Authors** : Alan Jessup
