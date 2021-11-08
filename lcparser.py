# Receives a raw lc string and parses it into a list-tree of terms.

class Parser:
    def __init__(self, rawlc):
        self.rawlc = rawlc
        self.tokens = []
        self.tokenize()
        self.tree = []
        self.parse_full()

    def tokenize(self):
        buff = ''
        for char in self.rawlc:
            if char in [';', '(', ')']:
                if buff:
                    self.tokens.append(buff)
                    buff = ''
                self.tokens.append(char)
            elif char == ' ' and buff:
                self.tokens.append(buff)
                buff = ''
            else:
                buff += char

    def eat_tokens(self, count):
        for i in range(0, count):
            del self.tokens[0]

    def parse_term(self):
        # don't need leading parens
        if self.tokens[0] == '(':
            self.eat_tokens(1)
        # fn x =>, LM
        if self.tokens[0] == 'fn':  # assumes tokens[2] is '=>'
            v = self.tokens[1]
            self.eat_tokens(3)
            return ['LM', v, self.parse_term()]
        # base case, last VA
        elif self.tokens[1] == ')':
            v = self.tokens[0]
            self.eat_tokens(2)
            return ['VA', v]
        # general case
        else:
            v = self.tokens[0]
            self.eat_tokens(1)
            return ['AP', ['VA', v], self.parse_term()]

    def parse_full(self):
        print(self.parse_term())

    def get_parsed(self):
        return self.tree
