from scanner import Scanner

scanner = Scanner()

def check_valid_path1():
    token = "\"/abc/def\""
    expected = ["<STRING, '\"/abc/def\"'>",]
    scanner.clear()
    actual,errors = scanner.scan(token)
    assert(actual == expected)

def check_valid_path2():
    token = "\"/hello_123/world-456\""
    expected = ["<STRING, '\"/hello_123/world-456\"'>",]
    scanner.clear()
    actual,errors = scanner.scan(token)
    assert(actual == expected)

def check_valid_path3():
    token = "\"/\""
    expected = ["<STRING, '\"/\"'>",]
    scanner.clear()
    actual,errors = scanner.scan(token)
    assert(actual == expected)

def check_valid_filepath():
    token = "\"/abc/def/file.txt\""
    expected = ["<STRING, '\"/abc/def/file.txt\"'>",]
    scanner.clear()
    actual,errors = scanner.scan(token)
    assert(actual == expected)

def check_string_against_path():
    token = "\"invalid\""
    expected = ["<STRING, '\"invalid\"'>",]
    scanner.clear()
    actual,errors = scanner.scan(token)
    assert(actual == expected)

def check_unclosed_string1():
    token = "\"abc,d"
    expected = []
    # expects errors

    scanner.clear()
    actual,errors = scanner.scan(token)
    assert(actual == expected)
    assert(len(errors) == 1)

def check_unclosed_string2():
    token = "abc,d\""
    expected = ["<IDENTIFIER, 'abc'>", "<SEPARATOR, ','>", "<IDENTIFIER, 'd'>"]
    # expects errors

    scanner.clear()
    actual,errors = scanner.scan(token)
    assert(actual == expected)
    assert(len(errors) == 1)

def check_unclosed_brackets():
    token = "define f(string dir {"
    expected = ["<KEYWORD, 'define'>",
                "<IDENTIFIER, 'f'>",
                "<SEPARATOR, '('>",
                "<KEYWORD, 'string'>",
                "<IDENTIFIER, 'dir'>",
                "<SEPARATOR, '{'>"]
    # expects syntax errors but not lexical errors

    scanner.clear()
    actual,errors = scanner.scan(token)
    assert(actual == expected)
    assert(len(errors) == 0)

def identifier_cannot_start_with_number():
    token = "123a"
    expected = []
    # expects errors, identifier cannot start with numbers

    scanner.clear()
    actual,errors = scanner.scan(token)
    assert (actual == expected)
    assert(len(errors) > 0)

def check_maximal_munch():
    token = "stringlist"
    expected = [
        "<IDENTIFIER, 'stringlist'>"
    ]

    scanner.clear()
    actual,errors = scanner.scan(token)
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

    scanner.clear()
    actual,errors = scanner.scan(program)
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
        "<STRING, '\"/home/Desktop\"'>",
        "<SEPARATOR, ';'>",
        "<KEYWORD, 'path'>",
        "<IDENTIFIER, 'directory2'>",
        "<OPERATOR, '='>",
        "<STRING, '\"/home/Documents\"'>",
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
        "<IDENTIFIER, 'rename_dirs'>",
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

    scanner.clear()
    actual,errors = scanner.scan(program)
    assert(actual == expected)


def test_all():
    check_valid_path1()
    check_valid_path2()
    check_valid_path3()
    check_valid_filepath()
    check_string_against_path()
    check_unclosed_string1()
    check_unclosed_string2()
    check_unclosed_brackets()
    identifier_cannot_start_with_number()
    check_maximal_munch()
    check_keyword_as_function_name()
    parse_complicated_program()

test_all()
