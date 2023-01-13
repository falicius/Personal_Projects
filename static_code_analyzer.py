import re
from collections import namedtuple
import os
import sys


CodeLine = namedtuple('CodeLine', 'ln_num line lines')


def S001(c: CodeLine):
    return len(c.line) > 79


def S002(c: CodeLine):
    regex = re.compile(r"^(?:\s{4})*\s{1,3}\S")
    return regex.search(c.line)


def S003(c: CodeLine):
    regex1 = re.compile(r"(.*)((;(\s)*#)|(;$))")
    regex2 = re.compile(r"#.*;")
    return regex1.search(c.line) and not regex2.search(c.line)


def S004(c: CodeLine):
    if re.match(r".+\s{2,}#.*", c.line):
        return None
    regex = re.compile(r"(([^ ]{2})|(\s[^ ])|([^ ]\s))#")
    return regex.search(c.line)


def S005(c: CodeLine):
    regex = re.compile(r"#(.*)todo", flags=re.IGNORECASE)
    return regex.search(c.line)


def S006(c: CodeLine):
    return c.lines[c.ln_num - 3:c.ln_num] == ['\n', '\n', '\n'] and c.line != "\n"


def S007(c: CodeLine):
    return re.search(r"(def|class)\s{2,}", c.line)


def S008(c: CodeLine):
    return re.match(r"class [a-z]+_?", c.line)


def S009(c: CodeLine):
    return re.search(r"def [A-Z]", c.line)


ERR_DESCS = {
    S001: 'Too Long',
    S002: 'Indentation is not a multiple of four',
    S003: 'Unnecessary semicolon',
    S004: 'At least two spaces before inline comments required',
    S005: 'TODO found',
    S006: 'More than two blank lines used before this line',
    S007: 'Too many spaces after construct',
    S008: 'Class name should use CamelCase',
    S009: 'Function name should use snake_case'
}


def main():
    path = str(sys.argv[1])
    if os.path.isfile(path) and path.endswith(".py"):
        check(path)
    elif os.path.isdir(path):
        dir_list = sorted(os.listdir(path))
        for file in dir_list:
            if file.endswith(".py") and re.match(r"test_", file):
                check(os.path.join(path, file))


def check(path):
    with open(f"{path}", "r") as file:
        lines = file.readlines()
        code_lines = [
            CodeLine(i, line, lines)
            for i, line in enumerate(lines)
        ]

    # Run all checks:
    errors = [
        error_message(c, f.__name__, desc, f(c), path)
        for c in code_lines
        for f, desc in ERR_DESCS.items()
    ]

    # Throw out all non-errors and print
    errors = list(filter(None, errors))
    for e in errors:
        print(e)


def error_message(c: CodeLine, name: str, desc: str, failed: bool, file: str):
    if failed:
        return f'{file}: Line {c.ln_num + 1}: {name} {desc}'
    return None


if __name__ == '__main__':
    main()
