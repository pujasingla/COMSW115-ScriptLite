import sys
import scanner

class ASTNode:
    def __init__(self, type, value = None):
        self.type = type
        self.value = value
        self.children = []
    
    def add_child(self, child):
        self.children.append(child)
    
    def __repr__(self, level=0):
        ret = " " * level + "|" + "─" * level + f"{self.type} ({self.value if self.value else ''})\n"
        for child in self.children:
            ret += child.__repr__(level + 1)
        return ret

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.declared_strings = set()
        self.declared_lists = set()
        self.declared_functions = set()

    def current_token(self):
        if self.pos < len(self.tokens):
            token_class, token_val = self.tokens[self.pos][1:-1].split(", ")
            return token_class, token_val[1:-1]
        return None
    
    def advance(self):
        self.pos += 1
    
    def roll_back(self):
        self.pos -= 1
    
    def print_err(self):
        print(f"Syntax error at token {self.current_token()}")

    def match(self, token_class, token_value = None):
        if self.current_token() and self.current_token()[0] == token_class \
            and (token_value is None or self.current_token()[1] == token_value):
            return self.current_token()
        return None

    def parse_program(self):
        root = ASTNode('PROGRAM')
        while self.current_token():
            node = self.parse_next()
            if node:
                root.add_child(node)
            else:
                self.print_err()
                break
        return root
    
    def parse_next(self):
        # Parse variable assignment
        if self.match('KEYWORD', 'string') or self.match('KEYWORD', 'list'):
            return self.parse_declaration()
        
        # Parse functions
        elif self.match('KEYWORD', 'define'):
            return self.parse_function()
        
        # Parse function calls
        elif self.match('KEYWORD', 'call'):
            return self.parse_function_call()
        
        # Parse statement
        else:
            return self.parse_statement()

    def parse_declaration(self):
        root = ASTNode('DECLARATION')
        if self.match('KEYWORD', 'string'):
            root.add_child(ASTNode('KEYWORD', "string"))
            self.advance()
            if self.match('IDENTIFIER'):
                root.add_child(ASTNode('IDENTIFIER', self.current_token()[1]))
                self.declared_strings.add(self.current_token()[1])
                self.advance()
            else:
                return
            if self.match('OPERATOR'):
                root.add_child(ASTNode('OPERATOR', self.current_token()[1]))
                self.advance()
            else:
                return
            if self.match('STRING'):
                root.add_child(ASTNode('STRING', self.current_token()[1]))
                self.advance()
            else:
                return

        else:
            root.add_child(ASTNode('KEYWORD', 'list'))
            self.advance()
            if self.match('IDENTIFIER'):
                root.add_child(ASTNode('IDENTIFIER', self.current_token()[1]))
                self.declared_lists.add(self.current_token()[1])
                self.advance()
            else:
                return
            if self.match('OPERATOR'):
                root.add_child(ASTNode('OPERATOR', self.current_token()[1]))
                self.advance()
            else:
                return
            node = self.parse_list()
            if node:
                root.add_child(node)
                self.advance()
            else:
                return

        if self.match('SEPARATOR', ';'):
            root.add_child(ASTNode('SEPARATOR', ';'))
            self.advance()    
        
        return root
    
    def parse_list(self):
        root = ASTNode('LIST')
        if self.match('SEPARATOR', '['):
            root.add_child(ASTNode('SEPARATOR', '['))
            self.advance()
            while self.current_token() and self.current_token()[1] != ']':
                if self.match('STRING'):
                    root.add_child(ASTNode('STRING', self.current_token()[1]))
                elif self.match('IDENTIFIER') and self.current_token()[1] in self.declared_strings:
                    root.add_child(ASTNode('IDENTIFIER', self.current_token()[1]))
                else:
                    print("noo", self.current_token())
                    self.print_err()
                    return
                self.advance()
                if self.current_token()[1] == ']':
                    root.add_child(ASTNode('SEPARATOR', ']'))
                    self.advance()
                    break
                if self.match('SEPARATOR', ','):
                    root.add_child(ASTNode('SEPARATOR', ','))
                    self.advance()       
            else:
                self.print_err()
                return  
            return root
        else:
            self.print_err()
            return
    
    def parse_function(self):
        return
    
    def parse_block(self):
        return
    
    def parse_param_list(self):
        return
    
    def parse_parameters(self):
        return
    
    def parse_statement(self):
        return
    
    def parse_expression(self):
        return
    
    def parse_function_call(self):
        return


if __name__ == "__main__":
    sample_program = """
    string directory1 = "/user/Desktop";
    string directory2 = "/home/user/Documents";
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