import sys
import scanner

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def parse_program(self):
        return


if __name__ == "__main__":
    sample_program = """
    string directory1 = "/user/Desktop";
    string directory2 = "/home/user/Documents"
    list directories = [directory1, directory2];
    string prefix = "prefix";

   define rename_files_in_dirs (list directories, string prefix)
   {
    bulk_rename_files file IN directories TO prefix + file;
   }

    call rename_files_in_dirs(directories);
    """

    # Run the scanner
    scanner = scanner.Scanner()
    tokens, errors = scanner.scan(sample_program)

    for token in tokens:
        print(token)

    if errors:
        for error in errors:
            print(error)
        sys.exit(1)

    # Run the parser
    parser = Parser(tokens)
    try:
        ast = parser.parse_program()
        print("\nGenerated AST:")
        print(ast)
    except SyntaxError as e:
        print(f"Syntax error: {e}")