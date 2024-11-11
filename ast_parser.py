import os
import sys
import scanner

class ASTNode:
    def __init__(self, type, value = None):
        self.type = type
        self.value = value
        self.children = []
    
    def add_child(self, child):
        self.children.append(child)
    
    def __repr__(self, level = 0):
        ret = "  " * level + "├" + "── " + f"{self.type} ({self.value if self.value else ''})\n"
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
    
    def print_err(self):
        print(f"Syntax error at token {self.current_token()}")

    def match_values(self, token_class, token_values = None):
        if token_values is None:
            token_values = []
        if self.current_token() and self.current_token()[0] == token_class \
            and (token_values == [] or self.current_token()[1] in token_values):
            return self.current_token()
        return None

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
            else:
                return

        if self.match('SEPARATOR', ';'):
            root.add_child(ASTNode('SEPARATOR', ';'))
            self.advance()
        else:
            self.print_err()
        
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
                return
        elif self.match('KEYWORD', 'get_files'):
            root.add_child(ASTNode('KEYWORD', 'get_files'))
            self.advance()
            if self.match('IDENTIFIER'):
                root.add_child(ASTNode('IDENTIFIER', self.current_token()[1]))
                self.advance()
        else:
            return
        return root
    
    def parse_function(self):
        root = ASTNode("FUNCTION")
        node = self.parse_function_header()
        if node:
            root.add_child(node)
        else:
            return
        root.add_child(self.parse_block())
        return root
    
    def parse_function_header(self):
        root = ASTNode('FUNC_HEADER')
        if self.match('KEYWORD', 'define'):
            root.add_child(ASTNode('KEYWORD', "define"))
            self.advance()

            if self.match('IDENTIFIER'):
                root.add_child(ASTNode('IDENTIFIER', self.current_token()[1]))
                self.declared_functions.add(self.current_token()[1])
                self.advance()
            else:
                return
            
            node = self.parse_param_list()
            if node:
                root.add_child(node)
            else:
                return

        return root
    
    def parse_param_list(self):
        root = ASTNode('PARAMETER_LIST')
        if self.match('SEPARATOR', '('):
            root.add_child(ASTNode('SEPARATOR', '('))
            self.advance()
            while self.current_token() and self.current_token()[1] != ')':
                node = self.parse_parameter()
                expecting_parameter = False
                if node:
                    root.add_child(node)

                if self.match('SEPARATOR', ','):
                    root.add_child(ASTNode('SEPARATOR', ','))
                    self.advance()
                    expecting_parameter = True
                else:
                    break
            if expecting_parameter:
                raise SyntaxError("Syntax Error: Trailing ',' with no parameter")

        else:
            return

        if self.match('SEPARATOR', ')'):
            root.add_child(ASTNode('SEPARATOR', ')'))
            self.advance()
        else:
            return
            
        return root
    
    def parse_parameter(self):
        root = ASTNode('PARAMETER')
        if self.match('KEYWORD', 'string'):
            root.add_child(ASTNode('KEYWORD', "string"))
            self.advance()
            if self.match('IDENTIFIER'):
                root.add_child(ASTNode('IDENTIFIER', self.current_token()[1]))
                self.declared_strings.add(self.current_token()[1])
                self.advance()
            else:
                return

        elif self.match('KEYWORD', 'list'):
            root.add_child(ASTNode('KEYWORD', 'list'))
            self.advance()
            if self.match('IDENTIFIER'):
                root.add_child(ASTNode('IDENTIFIER', self.current_token()[1]))
                self.declared_lists.add(self.current_token()[1])
                self.advance()
            else:
                return
        else:
            return

        return root
            
    def parse_block(self):
        root = ASTNode('BLOCK')
        if self.match('SEPARATOR', '{'):
            root.add_child(ASTNode('SEPARATOR', '{'))
            self.advance()
            while self.current_token() and self.current_token()[1] != '}':
                if self.match('KEYWORD', 'call'):
                    root.add_child(self.parse_function_call())
                    continue
                if self.match('KEYWORD', 'string') or self.match('KEYWORD', 'list'):
                    root.add_child(self.parse_declaration())
                    continue
                if self.match('KEYWORD', 'foreach'):
                    root.add_child(self.parse_foreach())
                    continue
                else:
                    root.add_child(self.parse_statement())
        else:
            raise SyntaxError("Syntax Error: Missing {")

        if self.match('SEPARATOR', '}'):
            root.add_child(ASTNode('SEPARATOR', '}'))
            self.advance()
        else:
            raise SyntaxError("Syntax Error: Missing }")

        return root

    def parse_statement(self):
        root = ASTNode('STATEMENT')
        acceptable_keywords_type_1 = ['create_directory','display_files', 'create_new_file','get_files']
        acceptable_keywords_type_2 = ['move_files', 'copy_files']
        if self.match_values('KEYWORD', acceptable_keywords_type_1):
            root.add_child(ASTNode('KEYWORD', self.current_token()[1]))
            self.advance()

            if self.match('IDENTIFIER'):
                root.add_child(ASTNode('IDENTIFIER', self.current_token()[1]))
                self.advance()
            elif self.match('STRING'):
                root.add_child(ASTNode('STRING', self.current_token()[1]))
                self.declared_strings.add(self.current_token()[1])
                self.advance()

        elif self.match_values('KEYWORD', acceptable_keywords_type_2):
            root.add_child(ASTNode('KEYWORD', self.current_token()[1]))
            self.advance()

            if self.match('IDENTIFIER'):
                root.add_child(ASTNode('IDENTIFIER', self.current_token()[1]))
                self.advance()
            else:
                return

            if self.match('KEYWORD','in'):
                root.add_child(ASTNode('KEYWORD', self.current_token()[1]))
                self.advance()
            else:
                return

            if self.match('IDENTIFIER'):
                root.add_child(ASTNode('IDENTIFIER', self.current_token()[1]))
                self.advance()
            else:
                return

            if self.current_token() and self.current_token()[1] == 'ends_with':
                if self.match('KEYWORD', 'ends_with'):
                    root.add_child(ASTNode('KEYWORD', self.current_token()[1]))
                    self.advance()
                else:
                    return

                if self.match('STRING'):
                    root.add_child(ASTNode('STRING', self.current_token()[1]))
                    self.advance()
                else:
                    return

            if self.match('KEYWORD','to'):
                root.add_child(ASTNode('KEYWORD', self.current_token()[1]))
                self.advance()
            else:
                return

            if self.match('IDENTIFIER'):
                root.add_child(ASTNode('IDENTIFIER', self.current_token()[1]))
                self.advance()
            else:
                return

        elif self.match('KEYWORD', 'append'):
            root.add_child(ASTNode('KEYWORD', self.current_token()[1]))
            self.advance()

            if self.match('IDENTIFIER'):
                root.add_child(ASTNode('IDENTIFIER', self.current_token()[1]))
                self.advance()
            else:
                return

            if self.match('KEYWORD', 'to'):
                root.add_child(ASTNode('KEYWORD', self.current_token()[1]))
                self.advance()
            else:
                return
            if self.match('IDENTIFIER'):
                root.add_child(ASTNode('IDENTIFIER', self.current_token()[1]))
                self.advance()
            else:
                return

        elif self.match('KEYWORD', 'add_content'):
            root.add_child(ASTNode('KEYWORD', self.current_token()[1]))
            self.advance()

            if self.match('STRING'):
                root.add_child(ASTNode('STRING', self.current_token()[1]))
                self.advance()
            else:
                return

            if self.match('KEYWORD', 'to'):
                root.add_child(ASTNode('KEYWORD', self.current_token()[1]))
                self.advance()
            else:
                return

            if self.match('IDENTIFIER'):
                root.add_child(ASTNode('IDENTIFIER', self.current_token()[1]))
                self.advance()
            elif self.match('STRING'):
                root.add_child(ASTNode('STRING', self.current_token()[1]))
                self.advance()
            else:
                return

        elif self.match('KEYWORD', 'bulk_rename_files'):
            root.add_child(ASTNode('KEYWORD', self.current_token()[1]))
            self.advance()

            if self.match('IDENTIFIER'):
                root.add_child(ASTNode('IDENTIFIER', self.current_token()[1]))
                self.advance()
            else:
                return

            if self.match('KEYWORD','in'):
                root.add_child(ASTNode('KEYWORD', self.current_token()[1]))
                self.advance()
            else:
                return
            if self.match('IDENTIFIER'):
                root.add_child(ASTNode('IDENTIFIER', self.current_token()[1]))
                self.advance()
            else:
                return

            if self.match('KEYWORD','to'):
                root.add_child(ASTNode('KEYWORD', self.current_token()[1]))
                self.advance()
            else:
                return
            root.add_child(self.parse_expression())

        else:
            raise SyntaxError(f"Syntax error at {self.current_token()[1]}")

        if self.match('SEPARATOR', ';'):
            root.add_child(ASTNode('SEPARATOR', ';'))
        else:
            raise SyntaxError(f"Missing semi-colon")
        self.advance()

        return root

    def parse_expression(self):
        root = ASTNode('EXPRESSION')
        if self.match('STRING'):
            root.add_child(ASTNode('STRING', self.current_token()[1]))
            self.advance()

            if self.match('OPERATOR'):
                root.add_child(ASTNode('OPERATOR', self.current_token()[1]))
                self.advance()
            else:
                return

            if self.match('IDENTIFIER'):
                root.add_child(ASTNode('IDENTIFIER', self.current_token()[1]))
                self.declared_strings.add(self.current_token()[1])
                self.advance()
            else:
                return

        elif self.match('IDENTIFIER'):
            root.add_child(ASTNode('IDENTIFIER', self.current_token()[1]))
            self.advance()

            if self.match('OPERATOR'):
                root.add_child(ASTNode('OPERATOR', self.current_token()[1]))
                self.advance()
            else:
                return
            if self.match('IDENTIFIER'):
                root.add_child(ASTNode('IDENTIFIER', self.current_token()[1]))
                self.declared_strings.add(self.current_token()[1])
                self.advance()
            else:
                return

        elif self.match('IDENTIFIER'):
            root.add_child(ASTNode('IDENTIFIER', self.current_token()[1]))
            self.advance()

            if self.match('OPERATOR'):
                root.add_child(ASTNode('OPERATOR', self.current_token()[1]))
                self.advance()
            else:
                return
            if self.match('STRING'):
                root.add_child(ASTNode('STRING', self.current_token()[1]))
                self.declared_strings.add(self.current_token()[1])
                self.advance()
            else:
                return
        elif self.match('STRING'):
            root.add_child(ASTNode('STRING', self.current_token()[1]))
            self.advance()

            if self.match('OPERATOR'):
                root.add_child(ASTNode('OPERATOR', self.current_token()[1]))
                self.advance()
            else:
                return
            if self.match('STRING'):
                root.add_child(ASTNode('STRING', self.current_token()[1]))
                self.declared_strings.add(self.current_token()[1])
                self.advance()
            else:
                return
        else:
            return

        return root
    
    def parse_function_call(self):
        root = ASTNode('FUNC_CALL')
        if self.match('KEYWORD', 'call'):
            root.add_child(ASTNode('KEYWORD', "call"))
            self.advance()

            if self.match('IDENTIFIER'):
                root.add_child(ASTNode('IDENTIFIER', self.current_token()[1]))
                # self.declared_functions.add(self.current_token()[1])
                self.advance()
            else:
                return

            node = self.parse_argument_list()
            if node:
                root.add_child(node)

        if self.match('SEPARATOR', ';'):
            root.add_child(ASTNode('SEPARATOR', ';'))
            self.advance()

        return root

    def parse_argument_list(self):
        root = ASTNode('ARGUMENTS')
        if self.match('SEPARATOR', '('):
            root.add_child(ASTNode('SEPARATOR', '('))
            self.advance()
            expecting_argument = True

            while self.current_token() and self.current_token()[1] != ')':
                if self.match('IDENTIFIER'):
                    root.add_child(ASTNode('IDENTIFIER', self.current_token()[1]))
                    self.declared_strings.add(self.current_token()[1])
                    self.advance()
                    expecting_argument = False

                if self.current_token()[1] == ')':
                    break
                if self.match('SEPARATOR', ','):
                    root.add_child(ASTNode('SEPARATOR', ','))
                    self.advance()
                    expecting_argument = True
            if expecting_argument:
                raise SyntaxError("Syntax Error: Trailing ',' with no argument")

        self.match('SEPARATOR', ')')
        root.add_child(ASTNode('SEPARATOR', ')'))
        self.advance()
        return root

    def parse_foreach(self):
        root = ASTNode('FOREACH')
        if self.match('KEYWORD', 'foreach'):
            root.add_child(ASTNode('KEYWORD', self.current_token()[1]))
            self.advance()
            while self.current_token():
                if self.match('IDENTIFIER'):
                    root.add_child(ASTNode('IDENTIFIER', self.current_token()[1]))
                    self.declared_functions.add(self.current_token()[1])
                    self.advance()
                    continue

                if self.match('KEYWORD', 'in'):
                    root.add_child(ASTNode('KEYWORD', self.current_token()[1]))
                    self.advance()
                    continue

                if self.match('IDENTIFIER'):
                    root.add_child(ASTNode('IDENTIFIER', self.current_token()[1]))
                    self.declared_functions.add(self.current_token()[1])
                    self.advance()
                    continue

                if self.match('SEPARATOR', '{'):
                    root.add_child(self.parse_block())
                    break

        else:
            return

        return root


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Argument missing: python3 ast_parser.py <input_file>")
        sys.exit(1)

    input_dir = "Parser_Input_Programs/"
    input_file = os.path.join(input_dir, sys.argv[1])

    try:
        with open(input_file, 'r') as file:
            program = file.read()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)

    # Run the scanner
    scanner = scanner.Scanner()
    tokens, errors = scanner.scan(program)

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