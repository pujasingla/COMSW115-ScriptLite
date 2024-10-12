from scanner import Scanner

scanner = Scanner()

def check_valid_path1():
    token = "/abc/def"
    expected = ["<PATH, '\"/abc/def\"'>",]
    actual = scanner.scan(token)
    assert(actual == expected)

def check_valid_path2():
    token = "/hello_123/world-456"
    expected = ["<PATH, '\"/hello_123/world-456\"'>",]
    actual = scanner.scan(token)
    assert(actual == expected)

def check_valid_path3():
    token = "/"
    expected = ["<PATH, '\"/\"'>",]
    actual = scanner.scan(token)
    assert(actual == expected)

def check_valid_filepath():
    token = "/abc/def/file.txt"
    expected = ["<PATH, '\"/abc/def/file.txt\"'>",]
    actual = scanner.scan(token)
    assert(actual == expected)

def check_string_against_path():
    token = "invalid"
    expected = ["<IDENTIFIER, '\"invalid\"'>",]
    actual = scanner.scan(token)
    assert(actual == expected)

def check_invalid_path1():
    # expects an error
    token = "/abc/def/"
    expected = []
    actual = scanner.scan(token)
    assert(actual == expected)

def check_invalid_path2():
    # expects an error
    token = "/abc//def/"
    expected = []
    actual = scanner.scan(token)
    assert(actual == expected)

def check_invalid_path3():
    # expects an error
    token = "//"
    expected = []
    actual = scanner.scan(token)
    assert(actual == expected)

def check_invalid_path4():
    # expects an error
    token = "abc/def"
    expected = []
    actual = scanner.scan(token)
    assert(actual == expected)

def check_invalid_path5():
    invalid_token = "/home//"
    expected = []
    # expects errors

    actual = scanner.scan(invalid_token)
    assert(actual == expected)

def check_invalid_token():
    token = "\"abc,d"
    expected = []
    # expects errors

    actual = scanner.scan(token)
    assert(actual == expected)

def check_maximal_munch():
    token = "stringlist"
    expected = [
        "<IDENTIFIER, 'stringlist'>"
    ]

    actual = scanner.scan(token)
    assert(actual == expected)

def check_keyword_as_function_name():
    # should raise a syntax error at semantic phase
    program = '''
        define bulk_rename_files(list directories){
        }
    '''

    expected = [
        "<KEYWORD, 'define'>",
        "<KEYWORD, 'bulk_rename_files'>",
        "<SEPARATOR, '('>",
        "<KEYWORD, 'list'>",
        "<IDENTIFIER, 'directories'>",
        "<SEPARATOR, ')'>",
        "<SEPARATOR, '{'>",
        "<SEPARATOR, '}'>",
    ]

    actual = scanner.scan(program)
    assert(actual == expected)

def parse_complicated_program():
    program = '''
        path directory1 = "/home/Desktop";
        path directory2 = "/home/Documents";
        list directories = [directory1, directory2];

        define rename_dirs(list directories) 
        {
        string prefix = "prefix";
        bulk_rename_files file in directories to prefix+file;
        }

        call rename_dirs(directories);
    '''

    expected = [
        "<KEYWORD, 'path'>",
        "<IDENTIFIER, 'directory1'>",
        "<OPERATOR, '='>",
        "<PATH, '\"/home/Desktop\"'>",
        "<SEPARATOR, ';'>",
        "<KEYWORD, 'path'>",
        "<IDENTIFIER, 'directory2'>",
        "<OPERATOR, '='>",
        "<PATH, '\"/home/Documents\"'>",
        "<SEPARATOR, ';'>",
        "<KEYWORD, 'list'>",
        "<IDENTIFIER, 'directories'>",
        "<OPERATOR, '='>",
        "<SEPARATOR, '['>",
        "<IDENTIFIER, 'directory1'>",
        "<SEPARATOR, ','>",
        "<IDENTIFIER, 'directory2'>",
        "<SEPARATOR, ']'>",
        "<SEPARATOR, ';'>",
        "<KEYWORD, 'define'>",
        "<KEYWORD, 'rename_dirs'>",
        "<SEPARATOR, '('>",
        "<KEYWORD, 'list'>",
        "<IDENTIFIER, 'directories'>",
        "<SEPARATOR, ')'>",
        "<SEPARATOR, '{'>",
        "<KEYWORD, 'string'>",
        "<IDENTIFIER, 'prefix'>",
        "<OPERATOR, '='>",
        "<STRING, '\"prefix\"'>",
        "<SEPARATOR, ';'>",
        "<KEYWORD, 'bulk_rename_files'>",
        "<IDENTIFIER, 'file'>",
        "<KEYWORD, 'in'>",
        "<IDENTIFIER, 'directories'>",
        "<KEYWORD, 'to'>",
        "<IDENTIFIER, 'prefix'>",
        "<OPERATOR, '+'>",
        "<IDENTIFIER, 'file'>",
        "<SEPARATOR, ';'>",
        "<SEPARATOR, '}'>",
        "<KEYWORD, 'call'>",
        "<IDENTIFIER, 'rename_dirs'>",
        "<SEPARATOR, '('>",
         "<IDENTIFIER, 'directories'>",
        "<SEPARATOR, ')'>",
        "<SEPARATOR, ';'>",
    ]

    actual = scanner.scan(program)
    assert(actual == expected)


def test_all():
    check_valid_path1()
    check_valid_path2()
    check_valid_path3()
    # check_valid_filepath()
    check_string_against_path()
    check_invalid_path1()
    check_invalid_path2()
    check_invalid_path3()
    check_invalid_path4()
    check_invalid_path5()
    check_invalid_token()
    check_maximal_munch()
    check_keyword_as_function_name()
    parse_complicated_program()

test_all()
