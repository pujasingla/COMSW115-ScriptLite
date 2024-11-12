# COMSW115-ScriptLite

Team Members: Puja Singla (ps3467), Ria Luo (xl3466)

Video demo for parser (Programming 2): https://drive.google.com/file/d/14Eowv9yAQSn401B3Jn-2aXUW_2a-pLG2/view?usp=drive_link

**ScriptLite** is a language designed to simplify file management with a clear, easy-to-understand syntax that abstracts away complex shell commands for users who may be less familiar with shell scripts. It supports basic file operation commands, such as creating new directories, moving files, and copying files, as well as more advanced operations like batch moving files, batch renaming files, backing up files, and syncing files. The goals of this language are to:

1. **Simplify file management** for users unfamiliar with shell scripts, enabling them to perform complex file operations like batch-copying, syncing, and backups without the need for loops or extensive scripting.

2. **Streamline complex batch file operations** with an easy syntax that requires fewer lines of code.

3. **Provide a natural language-like syntax** that minimizes errors and makes tasks easier to understand and execute.


---

## ScriptLite Lexical Grammar

The lexical grammar of ScriptLite defines the syntax rules for recognizing different types of tokens within the language. Below are the token types supported by ScriptLite, along with their definitions and examples.

### 1. Keywords
Keywords are reserved words in the ScriptLite language that have special meanings. They cannot be used as identifiers.

- **Token Type**: `KEYWORD`
- **Regex**: `(path| list| define| call| in| to| string| bulk_rename_files| create_directory| copy_files| sync_files| display_files| ends_with| not| where| append| get_files| foreach| create_new_file| add_content)`
  
- **Examples**: `path`, `list`, `define`, `call`, `in`, `to`, `string`, `bulk_rename_files`, `create_directory`, `copy_files`, `sync_files`, `display_files`, `ends_with`, `not`, `where`, `append`, `get_files`, `foreach`, `create_new_file`, `add_content`

### 2. Identifiers
Identifiers are names used to identify variables, functions, and other entities in the program. They can be composed of letters, digits, and underscores, but must not begin with a digit.

- **Token Type**: `IDENTIFIER`
- **Regex**: `[a-zA-Z_][a-zA-Z0-9_]*`
- **Rules**: 
  - Must start with a letter or underscore (`_`).
  - Can contain letters, digits, and underscores.
- **Examples**: `my_variable`, `_functionName`, `data123`

### 3. Strings
Strings are sequences of characters enclosed in double quotes. They can contain any characters except the newline character.

- **Token Type**: `STRING`
- **Regex**: `"[^\"]*"`
- **Rules**:
  - Must be enclosed in double quotes (`"`).
  - Supports escaping of double quotes and other special characters (to be implemented as needed).
- **Examples**: `"Hello, World!"`, `"File path: C:\Users\Username"`

### 4. Operators
Operators are symbols that represent computations or operations on operands. ScriptLite supports simple arithmetic and assignment operations.

- **Token Type**: `OPERATOR`
- **Regex**: `[+=]`
- **Examples**: `+`, `=`

### 5. Separators
Separators are characters used to separate tokens and denote the structure of the code.

- **Token Type**: `SEPARATOR`
- **Regex**: `[();,{}\[\]]`
- **Examples**: `(`, `)`, `{`, `}`, `;`, `,`, `[`, `]`

---
## ScriptLite Context Free Grammer
The grammar defined below outlines the structure of the language, demonstrating how programs are constructed using various production rules.
### Non-Terminals
`Program`, `Declarations`, `Function_Header`, `Parameter_List`, `Parameter`, `Function_Call`, `Arguments`, `Block`, `Block_Statements`, `Statement`, `Expression`, `File_Handling`, `Files`, `CP`, `Foreach_statement`, `A`, `String`

### Terminals
`list`, `string`, `id`, `=`, `[`, `]`, `;`, `get_files`, `define`, `(`, `)`, `call`, `,`, `{`, `}`, `create_directory`, `display_files`, `create_new_file`, `add_content`, `to`, `append`, `bulk_rename_files`, `in`, `+`, `copy_files`, `move_files`, `ends_with`, `foreach`, `"`

### Production Rules
Program → Declarations Function_Header Function_Call | Statement

Declarations → list id = [ id ]; | string id = String; | list id = get_files id;

Function_Header → define id (Parameter_List) Block

Parameter_List → ε | list id Parameter_List’ | string id Parameter

Parameter → ε | , Parameter_List

Function_Call → call id(Arguments);

Arguments → id | ,Arguments | ε

Block → { Block_Statements } | { }

Block_Statements → Statement | Function_Call | Declarations | Foreach_statement

Statement → create_directory A; | display_files A; | create_new_file A; | get_files A|  add_content String to A; | File_Handling | append id to id; | bulk_rename_files id in id to Expression; 

Expression → A + A

File_Handling → Files  id in id CP to id

Files → copy_files | move_files

CP → ends_with String | ε

Foreach_statement → foreach id in id Block

A → String | id

String → “id”

### Parsing Algorithm
The program processes tokens from the scanner output and builds an Abstract Syntax Tree (AST) by recursively analyzing the structure of the source code. It matches tokens based on their class (e.g., KEYWORD, IDENTIFIER, etc.), advancing through the tokens while constructing nodes in the AST. Each node represents a syntactic construct like a variable declaration, function call, or block of code. The recursive
algorithm closely follows the production rule we defined above.

### Error Handling of Parser
Error handling is done using SyntaxError exceptions when the expected token doesn't match the current token. This ensures the parser detects and reports syntax errors, such as missing or misplaced tokens (e.g., missing semicolons or unbalanced parentheses). Some examples:
1. **Missing Semicolon:**
   ```plaintext
   string x = "hello"
   ```

2. **Unexpected Token:**
   ```plaintext
   list y = ;
   ```

3. **Mismatched Parentheses in Function Call:**
   ```plaintext
   call print("hello", 
   ```

4. **Trailing Comma in Parameter List:**
   ```plaintext
   define myFunction(string x, string y, )
   ```

5. **Incorrect Block Closure:**
   ```plaintext
   if condition {
       doSomething();
   ```

More examples can be found in the demo video linked at the top of README. 

## Description of the Scanner

### Cursor

The cursor keeps track of the current position in the input program string.
It increments as characters are processed.

### Tokens and Errors

- **Tokens**: A list that stores recognized tokens as tuples of (token type, token value).
- **Errors**: A list that records any lexical errors encountered during scanning.

## States and Transitions

The scanner transitions between different states based on the character being
analyzed. The main states can be summarized as follows:

### State Transitions

#### Whitespace State

- **Transition**: If the character is whitespace, the scanner simply advances
  the cursor to skip over it.

#### Identifier/Keyword State

- **Transition**: When the character is alphanumeric or an underscore, the scanner identifies the beginning of an
  identifier or keyword.
    - The scanner records the starting position of the potential token and enters a loop to collect all contiguous
      alphanumeric characters or underscores, forming a complete lexeme.
    - After exiting the loop, the scanner checks if the lexeme is present in the predefined set of keywords. If it is, a
      `KEYWORD` token is created. If not, it further checks if the lexeme starts with a digit. If it does, an error is
      logged, as identifiers cannot start with a number. Otherwise, the lexeme is classified as an `IDENTIFIER`, and the
      corresponding token is added.

#### String State

- **Transition**: If the character is a double quote (`"`), the scanner
  recognizes the start of a string literal.
    - It advances the cursor and enters a loop until it finds the closing quote,
      collecting characters for the string.
    - If it reaches the end of the line without finding the closing quote,
      it records a lexical error for an unclosed string.

#### Separator State

- **Transition**: If the character is found in the separators string,
  it recognizes it as a separator and adds it as a `SEPARATOR` token.

#### Operator State

- **Transition**: If the character is found in the operators string, it
  recognizes it as an operator and adds it as an `OPERATOR` token.

#### Error State

- **Transition**: If the character does not match any of the above criteria, it’s
  considered an invalid character. The scanner records an error and advances the cursor.

### Error Handling

- The scanner catches three main types of errors: invalid characters that do not
conform to any recognized token types, identifiers starting with numbers and unclosed string literals. When an
invalid character is encountered, it logs a lexical error message indicating
the character's position and type, allowing the scanner to continue processing
the remainder of the input without interruption. For identifiers starting with numbers it will throw an error stating
that identifier cannot start with numbers. For unclosed strings, the scanner
detects when a string literal begins with a double quote but lacks a corresponding
closing quote by the end of the line, recording this as an error as well.
In all the cases, the scanner advances the cursor to the next character after
logging the error, ensuring that it can continue scanning the input rather than
halting on encountering an error.
---
## Python Installation Steps

### macOS

To install Python on macOS using Homebrew:

1. **Install Homebrew** (if not already installed):
   Open Terminal and run:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```
2. Install Python
   ```bash
    brew install python
   ```

### Linux
To install Python on linux distribution:
```bash
sudo apt update
sudo apt install python3 python3-pip -y
```

### Verify Installation

After installation, verify that Python was installed correctly by running:

```bash
python3 --version
```
---
## Executing Shell Script (5 Example Programs)
To make the script executable, run the following command:

Lexer:
```bash
chmod +x run_lexer.sh
```

Parser: 
```bash
chmod +x ast_parser.sh
```

 Following are the description of each program and the command to execute the program. The expected output for each program for scanner is given in `expected_output.txt` file.

### Add copyright to directories program

This **ScriptLite** program automates the process of appending a copyright notice to all files within multiple directories. Below is a summary of its functionality:

- **Directories List**: The program defines a list of directories (`/user/Docs`, `/user/Projects`, `/user/Reports`) where the copyright notice will be appended.

- **Copyright Notice**: It also defines a `copyright_notice` string that contains the text `© 2024 Your Company. All rights reserved.` This notice will be added to each file in the specified directories.

Function Definitions:
1. **`append_copyright_to_file`**: Appends the `copyright_notice` string to a single file located at the `file_path`.

2. **`append_copyright_to_directory`**: Retrieves all files in a specified directory and iterates through each file, appending the copyright notice by calling `append_copyright_to_file`.

3. **`append_copyright_to_multiple_directories`**: Loops through each directory in the `directories` list and calls `append_copyright_to_directory` to append the copyright notice to all files in those directories.

Execution:
The program calls the `append_copyright_to_multiple_directories` function, which processes all the files across the listed directories and appends the copyright notice to them.

```bash
./run_lexer.sh add_copyright_to_directories.txt  
```
```bash
./run_parser.sh adding_copyright_to_directories.txt   
```

### Add new file program

This script performs basic file management tasks using the `ScriptLite` language. It demonstrates the following operations:

1. **Creating a Directory**: The program creates a new directory named `tasks`.
2. **Displaying Files**: It displays the contents of the `tasks` directory.
3. **Defining a Filename**: The filename `todo_list.txt` is assigned to the variable `file_name`.
4. **Creating a New File**: A new file named `todo_list.txt` is created in the `tasks` directory.
5. **Adding Content to the File**: The program adds the content `"finish programming assignment"` to the `todo_list.txt` file.

```bash
./run_lexer.sh adding_newfile\(errors_included\).txt
```
```bash
./run_parser.sh adding_newfile.txt 
```

### Backup Log files program

This ScriptLite program is designed to facilitate basic file management tasks, specifically creating directories and managing file copies. The script performs the following operations:

1. **Create a Backup Directory**: It initializes a string variable `dest_dir` with the path `/home/backup` and creates a directory at this location.
2. **Display Backup Directory Contents**: The program then lists all files present in the `/home/backup` directory to show the current contents.
3. **Set Source Directory**: It defines another string variable `src_dir` to point to the directory `/home/usr`.
4. **Copy Log Files**: The script copies all files ending with the `.log` extension from the `src_dir` to the `dest_dir`.
5. **Show Updated Backup Directory Contents**: Finally, it displays the contents of the `dest_dir` again to reflect any newly copied files.

```bash
./run_lexer.sh backup_log_files.txt
```
```bash
./run_parser.sh backup_log_files\(error\).txt 
```
### Bulk Rename Files Program
This ScriptLite program is designed to rename files in specified directories by adding a prefix to their original names. It starts by defining two directory paths, directory1 and directory2, which point to locations on a user's computer. It then creates a list named directories that includes these two directories.

The core functionality is encapsulated in the function rename_files_in_dirs, which takes a list of directories and a string prefix as parameters. Inside this function, the command bulk_rename_files is called to rename all files in the specified directories by appending the given prefix to each file name. Finally, the program invokes the rename_files_in_dirs function, passing in the directories list and the desired prefix.
```bash
 ./run_lexer.sh bulk_rename_files\(errors_included\).txt
```
```bash
 ./run_parser.sh bulk_rename_files\(error\).txt 
```

### Organize files by extension program

This ScriptLite program is designed to organize files in a specified source directory by categorizing them into separate folders based on their file types. The program defines four main functions to handle different file formats:

1. **`organize_jpg_files`**: Creates a directory for JPEG files and moves all `.jpg` files from the source directory to this new directory.

2. **`organize_pdf_files`**: Creates a directory for PDF files and moves all `.pdf` files from the source directory to this directory.

3. **`organize_docx_files`**: Creates a directory for DOCX files and moves all `.docx` files from the source directory to this directory.

4. **`organize_all_files`**: Calls the previous three functions to ensure that all specified file types are organized into their respective folders.

The program concludes by calling the `organize_all_files` function, passing the source and target directories as arguments. This automates the file organization process, making it easier for users to manage and find their files.

```bash
 ./run_lexer.sh organize_files_by_extension.txt
```
```bash
 ./run_parser.sh organize_files_by_extension\(error\).txt 
```

---

