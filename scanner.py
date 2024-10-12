SEPARATORS = {
    '(': 'LPAR',
    ')': 'RPAR',
    '{': 'LBRKT',
    '}': 'RBRKT',
    '[': 'LSQBRKT',
    ']': 'RSQBRKT',
    ',': 'COMMA',
    ';': 'SEMICOLON'
}

OPERATORS = {
    '+': 'PLUS',
    '=': 'EQUAL'
}

class Scanner:
    def __init__(self):
        self.cursor = 0
    
    def advance(self):
        self.cursor += 1
    
    def reset_cursor(self):
        self.cursor = 0
    
    def scan_one(self, token):
        return
    
    def scan(self, program):
        for line in program.split("\n"):
            self.reset_cursor()
            c = line[self.cursor]
            # look up state transitions


if __name__== "__main__":
    scanner = Scanner()
