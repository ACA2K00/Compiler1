class Tokens:
    tokens = None

    def __init__(self):
        self.tokens = []
    
    def append(self, token):
        self.tokens.append(token)

    def peek(self):
        return self.tokens[0]['type']

    def match(self, symb):
        token = self.tokens.pop(0)
        if token['type'] != symb:
            print("ERROR: EXPECTED Token")
            exit()
        return token
    
    def __str__(self):
        ret = ""
        for token in self.tokens:
            ret += token['type']
            if 'val' in token:
                ret += ":" + token['val']
            ret += '\n'
        return ret