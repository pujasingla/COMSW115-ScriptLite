import os
import sys
from ast_parser import Parser, ASTNode
from scanner import Scanner

class Generator:
    def __init__(self, ast):
        self.ast = ast
        self.global_vars2type = {}
        self.funcs_vars2type = {} # maps function name to a dict of vars2type
    
    def generate(self):
        return self.generate_node(self.ast)

    def generate_node(self, node):
        if node.type == 'PROGRAM':
            return self.generate_program(node)
        elif node.type == 'DECLARATION':
            return self.generate_declaration(node)
        elif node.type == 'FUNCTION':
            return self.generate_function(node)
        elif node.type == 'FUNC_CALL':
            return self.generate_function_call(node)
        elif node.type == 'STATEMENT':
            return self.generate_statement(node)
        elif node.type == 'EXPRESSION':
            return self.generate_expression(node)
        elif node.type == 'FOREACH':
            return self.generate_foreach(node)
        else:
            return ""

    def generate_program(self, node):
        return '\n'.join([self.generate_node(child) for child in node.children])

    def generate_declaration(self, node):
        # Handle string or list declarations.
        declaration_type = node.children[0].value
        var_name = node.children[1].value

        if declaration_type == 'string':
            value = node.children[3].value
            self.global_vars2type[var_name] = "string"
            return f"{var_name}={value}"
        elif declaration_type == 'list':
            list_items = []
            for child in node.children[3].children:
                if child.type == 'STRING':
                    list_items.append(child.value)
                elif child.type == 'IDENTIFIER':
                    list_items.append(f"\"${child.value}\"")
            self.global_vars2type[var_name] = "list"
            return f"{var_name}=({' '.join(list_items)})"
        return ""

    def generate_function(self, node):
        # Handle function definition.
        func_name, params = self.read_function_header(node.children[0])
        func_header = f"function {func_name}()\n"
        block = self.generate_block(node.children[1], params, func_name)

        return f"{func_header}{{\n{block}\n}}"
    
    def read_function_header(self, node):
        func_name = node.children[1].value
        self.funcs_vars2type[func_name] = {} # used to check if value passed into param is of correct type
        params = []
        for child in node.children[2].children:
            if child.type == 'PARAMETER':
                data_type = child.children[0].value
                var = child.children[1].value
                self.funcs_vars2type # used to check if value passed into param is of correct type
                self.funcs_vars2type[func_name][var] = data_type
                params.append(var)
        return func_name, params

    def generate_function_call(self, node):
        # Handle function calls.
        func_name = node.children[1].value
        args = []
        for child in node.children[2].children:
            if child.type == 'IDENTIFIER':
                if self.global_vars2type[child.value] == "string":
                    args.append(f"\"${child.value}\"")
                else:
                    args.append(f"\"${{{child.value}[@]}}\"")
        return f"{func_name} {' '.join(args)}"

    def generate_statement(self, node):
        # Handle the different types of statements like create_directory, display_files, etc.
        keyword = node.children[0].value
        if keyword in ['create_directory', 'display_files', 'create_new_file']:
            var_name = node.children[1].value if len(node.children) > 1 else node.children[1].value
            return f"{keyword} {var_name}"

        elif keyword in ['move_files', 'copy_files']:
            source = node.children[1].value
            destination = node.children[3].value
            return f"{keyword} {source} {destination}"

        elif keyword == 'append':
            source = node.children[1].value
            destination = node.children[3].value
            return f"\techo \"${source}\" >> \"${destination}\""

        elif keyword == 'bulk_rename_files':
            # TODO: replace with correct implementation
            source_dir = node.children[1].value
            target_dir = node.children[3].value
            return f"\trename {source_dir} {target_dir}"

        return ""

    def generate_block(self, node, params, func_name):
        # TODO: check if var defined in local or global variable checking and error handling
        param_lines = "\n".join([f"\t{param}=${i+1}" if self.funcs_vars2type[func_name][param] == "string" 
                                 else f"\t{param}=(\"$@\")" for i, param in enumerate(params)])
        
        # TODO: generate block code and add local vars to self.funcs_vars2type[func_name]
        return param_lines + '\n'.join([self.generate_node(child) for child in node.children])

    def generate_expression(self, node):
        # Handle expressions, typically a string or identifier with an operator.
        if len(node.children) == 1:
            return self.generate_node(node.children[0])
        elif len(node.children) == 3:
            left = self.generate_node(node.children[0])
            op = node.children[1].value
            right = self.generate_node(node.children[2])
            return f"{left} {op} {right}"
        return ""

    def generate_foreach(self, node):
        # Handle foreach loops.
        var_name = node.children[1].value
        list_name = node.children[3].value
        # TODO: for-loop block code, variable type checking
        block = self.generate_node(node.children[4])

        return f"\tfor {var_name} in \"${{{list_name}[@]}}\"; do\n{block}\n\tdone"


if __name__ == "__main__":
    # if len(sys.argv) != 2:
    #     print("Argument missing: python3 ast_parser.py <input_file>")
    #     sys.exit(1)

    # input_dir = "Parser_Input_Programs/"
    # input_file = os.path.join(input_dir, sys.argv[1])

    # try:
    #     with open(input_file, 'r') as file:
    #         program = file.read()
    # except FileNotFoundError:
    #     print(f"Error: File '{input_file}' not found.")
    #     sys.exit(1)

    # Run the scanner
    scanner = Scanner()
    program = '''
        list directories = ["/user/Docs", "/user/Projects", "/user/Reports"];
        string copyright_notice = "© 2024 Your Company. All rights reserved.";

        define append_copyright_to_file (string file_path, string copyright_notice)
        {
            append copyright_notice to file_path;
        }

        define append_copyright_to_directory (string directory, string copyright_notice)
        {
            list all_files = get_files directory;
            foreach file in all_files {
                call append_copyright_to_file(file, copyright_notice);
            }
        }

        define append_copyright_to_multiple_directories (list directories, string copyright_notice)
        {
            foreach directory in directories {
                call append_copyright_to_directory(directory, copyright_notice);
            }
        }

        call append_copyright_to_multiple_directories(directories, copyright_notice);
    '''
    program2 = '''
        string directory1 = "/user/Desktop";
        string directory2 = "/home/user/Documents";
        list directories = [directory1, directory2];
        string prefix = "prefix";

        define rename_files_in_dirs (list directories, string prefix) {

            bulk_rename_files file in directories to prefix + file;
        }
        call rename_files_in_dirs(directories, prefix);
        '''
    tokens, errors = scanner.scan(program2)

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
        sys.exit(1)

    # Generate the shell script from the AST
    generator = Generator(ast)
    shell_script = generator.generate()
    print("\nGenerated Shell Script:")
    print(shell_script)
