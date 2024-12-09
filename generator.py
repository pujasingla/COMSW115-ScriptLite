import os
import subprocess
import sys

from ast_parser import Parser
from scanner import Scanner

class Generator:
    def __init__(self, ast):
        self.ast = ast
        self.global_vars2type = {}
        self.funcs_vars2type = {} # maps function name to dir1 dict of vars2type
        self.func_calls = []
    
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
            for i, child in enumerate(node.children[3].children):
                if child.type == 'STRING':
                    list_items.append(child.value)
                elif child.type == 'IDENTIFIER':
                    if i>0 and node.children[3].children[i - 1].value == 'get_files':
                        list_items.append(f"\"${child.value}\"/*")
                    else:
                        list_items.append(f"\"${child.value}\"")

            self.global_vars2type[var_name] = "list"
            return f"\t{var_name}=({' '.join(list_items)})"
        return ""

    def generate_function(self, node):
        # Handle function definition.
        func_name, params = self.read_function_header(node.children[0])
        func_header = f"function {func_name}()\n"
        block = self.generate_function_block(node.children[1], params, func_name)

        return f"{func_header}{{\n{block}\n}}"
    
    def read_function_header(self, node):
        func_name = node.children[1].value
        self.funcs_vars2type[func_name] = {} # used to check if value passed into param is of correct type
        params = []
        for child in node.children[2].children:
            if child.type == 'PARAMETER':
                data_type = child.children[0].value
                var = child.children[1].value
                self.funcs_vars2type[func_name][var] = data_type
                params.append(var)
        return func_name, params

    def generate_function_call(self, node):
        # Handle function calls.
        func_name = node.children[1].value
        args = []
        for child in node.children[2].children:
            if child.type == 'IDENTIFIER':
                if self.global_vars2type.keys().__contains__(child.value) and self.global_vars2type[child.value] == "list":
                    args.append(f"\"${{{child.value}[@]}}\"")
                else:
                    args.append(f"\"${child.value}\"")
        self.func_calls.append(func_name)
        return f"\t{func_name} {' '.join(args)}"

    def generate_statement(self, node):
        # Handle the different types of statements like create_directory, display_files, etc.
        keyword = node.children[0].value
        if keyword in ['create_directory']:
            if node.children[1].type == 'IDENTIFIER':
                return f'\tmkdir "${node.children[1].value}"'
            elif node.children[1].type == 'STRING':
                return f"\tmkdir {node.children[1].value}"

        elif keyword in ['display_files']:
            if node.children[1].type == 'STRING':
                return f"\tls {node.children[1].value}"
            elif node.children[1].type == 'IDENTIFIER':
                return f"\tls ${node.children[1].value}"

        elif keyword in ['move_files']:
            return f'\tfind "${node.children[3].value}" -type f -name "*{node.children[5].value[1:len(node.children[5].value)-1]}" -exec mv {{}} "${node.children[7].value}" \\;'

        elif keyword in ['copy_files']:
            return f'\tfind "${node.children[3].value}" -type f -name "*{node.children[5].value[1:len(node.children[5].value)-1]}" -exec cp {{}} "${node.children[7].value}" \\;'

        elif keyword in ['create_new_file']:
            if node.children[1].type == 'STRING':
                return f"\ttouch {node.children[1].value}"
            elif node.children[1].type == 'IDENTIFIER':
                return f"\ttouch ${node.children[1].value}"

        elif keyword in ['add_content']:
            return f"echo \"{node.children[1].value}\" >> ${node.children[3].value}"

        elif keyword == 'append':
            source = node.children[1].value
            destination = node.children[3].value
            return f"\techo \"${source}\" >> \"${destination}\""



        elif keyword == 'bulk_rename_files':
            return self.generate_bash_code_for_bulk_rename(node.children[3].value, node.children[5].children[0].value)

        return ""

    def generate_bash_code_for_bulk_rename(self, directories, prefix):
        bash_code = f"""
    for dir in "${{{directories}[@]}}"; do
        if [ -d "$dir" ]; then
            for file in "$dir"/*; do
                if [ -f "$file" ]; then
                    base_name=$(basename "$file")
                    mv "$file" "$dir/${{prefix}}_$base_name"
                fi
            done
        else
            echo "Directory $dir does not exist."
        fi
    done
    """
        return bash_code.strip()

    def generate_function_block(self, node, params, func_name):
        first_param = params[0]
        first_param_type = self.funcs_vars2type[func_name][first_param]
        if first_param_type == 'list':
            param_lines = "\n".join([f'\tlocal {param}=("${{@:1:$(($#-1))}}")'
                if self.funcs_vars2type[func_name][param] != "string"
                else f'\tlocal {param}=(\"${{@: -1}}")' for param in params])
        else:
            param_lines = "\n".join([f'\tlocal {param}="${i+1}"' for i, param in enumerate(params)])
        
        return param_lines + '\n'.join([self.generate_node(child) for child in node.children])

    def generate_expression(self, node):
        # Handle expressions, typically dir1 string or identifier with an operator.
        if len(node.children) == 1:
            return self.generate_node(node.children[0])
        elif len(node.children) == 3:
            left = self.generate_node(node.children[0])
            op = node.children[1].value
            right = self.generate_node(node.children[2])
            return f"{left} {op} {right}"
        return ""

    def generate_block(self, node):
        for child in node.children:
            if child.type == 'SEPARATOR':
                continue
            else:
                return self.generate_node(child)

    def generate_foreach(self, node):
        var_name = node.children[1].value
        list_name = node.children[3].value
        self.global_vars2type[var_name] = "list"
        block = self.generate_block(node.children[4])

        return f"\tfor {var_name} in \"${{{list_name}[@]}}\"; do\n{block}\n\tdone"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Argument missing: python3 generator.py <input_file>")
        sys.exit(1)

    input_dir = "CodeGeneration_Input_Programs/"
    input_file = os.path.join(input_dir, sys.argv[1])

    try:
        with open(input_file, 'r') as file:
            program = file.read()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)

    # Run the scanner
    scanner = Scanner()
    tokens, errors = scanner.scan(program)

    if errors:
        for error in errors:
            print(error)
        sys.exit(1)

    # Run the parser
    parser = Parser(tokens)
    try:
        ast = parser.parse_program()
        # print("\nGenerated AST:")
        # print(ast)
    except SyntaxError as e:
        print(f"Syntax error: {e}")
        sys.exit(1)

    # Generate the shell script from the AST
    generator = Generator(ast)
    shell_script = generator.generate()
    print(shell_script)
    file_path = "generated_shell_script.sh"
    with open(file_path, "w") as file:
        file.write(shell_script)

    try:
        # Run the script with the shell interpreter
        subprocess.run(["bash", file_path], check=True)
        print(f"Script {file_path} executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while executing {file_path}: {e}")
