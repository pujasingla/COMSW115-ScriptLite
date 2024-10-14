import sys

class Scanner:
    def __init__(self):
        self.cursor = 0
        self.tokens = []
        self.errors = []

    def clear(self):
        #For testing purposes
        self.tokens = []
        self.errors = []

    def advance(self):
        self.cursor += 1

    def reset_cursor(self):
        self.cursor = 0

    def add_tokens(self, token_type, token_value):
        self.tokens.append((token_type, token_value))
    
    def get_errors(self):
        return self.errors

    def scan(self, program):
        keywords = {'path', 'list', 'define', 'call', 'in', 'to', 'string', 
                    'bulk_rename_files', 'create_directory', 'copy_files', 
                    'sync_files', 'display_files', 'ends_with', 'not', 'where'}
        separators = "();,{}[]"
        operators = "+="

        for line in program.split("\n"):
            self.reset_cursor()
            line_length = len(line)

            while self.cursor < line_length:
                c = line[self.cursor]

                # Whitespace handling
                if c.isspace():
                    self.advance()
                    continue

                # Identifier/Keyword State
                elif c.isalpha() or c == '_':
                    token_start = self.cursor
                    while self.cursor < line_length and (line[self.cursor].isalnum() or line[self.cursor] == '_'):
                        self.advance()
                    lexeme = line[token_start:self.cursor]
                    if lexeme.lower() in keywords:
                        self.add_tokens('KEYWORD', lexeme)
                    else:
                        self.add_tokens('IDENTIFIER', lexeme)
                    continue

                # String State
                elif c == '"':
                    token_start = self.cursor
                    self.advance()
                    while self.cursor < line_length and line[self.cursor] != '"':
                        self.advance()
                    if self.cursor < line_length:
                        self.advance()
                        lexeme = line[token_start:self.cursor]
                        self.add_tokens('STRING', lexeme)
                    else:
                        self.errors.append(f"Lexical error: unclosed string at position {token_start}")
                    continue

                # Separator State
                elif c in separators:
                    self.add_tokens('SEPARATOR', c)
                    self.advance()
                    continue

                # Operator State
                elif c in operators:
                    self.add_tokens('OPERATOR', c)
                    self.advance()
                    continue

                # Error State
                else:
                    self.errors.append(f"Lexical error at position {self.cursor}: invalid character '{c}'")
                    self.advance()

        output = []
        for tkn in self.tokens:
            output.append('<' + tkn[0] + ', \'' + tkn[1] + '\'>')

        return output


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Argument missing: python scanner.py <input_program_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        with open(input_file, 'r') as file:
            program = file.read()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)

    scanner = Scanner()
    output = scanner.scan(program)

    for token in output:
        print(token)

    for error in scanner.errors:
        print(error)