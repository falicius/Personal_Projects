import re
import os
import sys


def main():
    arg = str(sys.argv[1])
    analyze_pathname(arg)


def analyze_pathname(pathname: str):
    if os.path.isfile(pathname):
        return analyze_file(pathname)

    if os.path.isdir(pathname):
        scripts: list = sorted(os.listdir(pathname))
        for script in scripts:
            script_path: str = os.path.join(pathname, script)
            analyze_file(script_path)


def analyze_file(filename: str):
    preceding_blank_line_counter: int = 0
    with open(filename) as file:
        for i, line in enumerate(file, start=1):
            if line == "\n":
                preceding_blank_line_counter += 1
                continue

            error_source: str = f"{filename}: Line {i}:"

            if len(line) > 79:
                print(error_source, "S001 Too long")

            if re.match(r"(?!^( {4})*[^ ])", line):
                print(error_source, "S002 Indentation is not a multiple of four")

            if re.search(r"^([^#])*;(?!\S)", line):
                print(error_source, "S003 Unnecessary semicolon")

            if re.match(r"[^#]*[^ ]( ?#)", line):
                print(error_source, "S004 At least two spaces before inline comment required")

            if re.search(r"(?i)# *todo", line):
                print(error_source, "S005 TODO found")

            if preceding_blank_line_counter > 2:
                print(error_source, "S006 More than two blank lines used before this line")
            preceding_blank_line_counter = 0

            if re.match(r"^([ ]*(?:class|def) ( )+)", line):
                print(error_source, "S007 Too many spaces after construction_name (def or class)")

            if matches := re.match(r"^(?:[ ]*class (?P<name>\w+))", line):
                if not re.match(r"(?:[A-Z][a-z0-9]+)+", matches["name"]):
                    print(error_source, f'S008 Class name {matches["name"]} should use CamelCase')

            if matches := re.match(r"^(?:[ ]*def (?P<name>\w+))", line):
                if not re.match(r"[a-z_]+", matches["name"]):
                    print(error_source, f'S009 Function name {matches["name"]} should use snake_case')

            if matches := re.search(r"\(.*(?P<name>[A-Z][\w]*)\s?=", line):
                print(error_source, f'S010 Argument name {matches["name"]} should be written in snake_case')

            if matches := re.match(r"^\s*(?P<name>[A-Z][\w]*)[\w\s]*=", line):
                print(error_source, f'S011 Variable {matches["name"]} should be written in snake_case')

            if re.search(r"[\w]*\s?=\[]", line):
                print(error_source, f'S012 The default argument value is mutable')


if __name__ == '__main__':
    main()


    
    
    
    
    

# import re
# from collections import namedtuple
# import os
# import sys


# CodeLine = namedtuple('CodeLine', 'ln_num line lines')


# def S001(c: CodeLine):
#     return len(c.line) > 79


# def S002(c: CodeLine):
#     regex = re.compile(r"^(?:\s{4})*\s{1,3}\S")
#     return regex.search(c.line)


# def S003(c: CodeLine):
#     regex1 = re.compile(r"(.*)((;(\s)*#)|(;$))")
#     regex2 = re.compile(r"#.*;")
#     return regex1.search(c.line) and not regex2.search(c.line)


# def S004(c: CodeLine):
#     if re.match(r".+\s{2,}#.*", c.line):
#         return None
#     regex = re.compile(r"(([^ ]{2})|(\s[^ ])|([^ ]\s))#")
#     return regex.search(c.line)


# def S005(c: CodeLine):
#     regex = re.compile(r"#(.*)todo", flags=re.IGNORECASE)
#     return regex.search(c.line)


# def S006(c: CodeLine):
#     return c.lines[c.ln_num - 3:c.ln_num] == ['\n', '\n', '\n'] and c.line != "\n"


# def S007(c: CodeLine):
#     return re.search(r"(def|class)\s{2,}", c.line)


# def S008(c: CodeLine):
#     return re.match(r"class [a-z]+_?", c.line)


# def S009(c: CodeLine):
#     return re.search(r"def [A-Z]", c.line)


# ERR_DESCS = {
#     S001: 'Too Long',
#     S002: 'Indentation is not a multiple of four',
#     S003: 'Unnecessary semicolon',
#     S004: 'At least two spaces before inline comments required',
#     S005: 'TODO found',
#     S006: 'More than two blank lines used before this line',
#     S007: 'Too many spaces after construct',
#     S008: 'Class name should use CamelCase',
#     S009: 'Function name should use snake_case'
# }


# def main():
#     path = str(sys.argv[1])
#     if os.path.isfile(path) and path.endswith(".py"):
#         check(path)
#     elif os.path.isdir(path):
#         dir_list = sorted(os.listdir(path))
#         for file in dir_list:
#             if file.endswith(".py") and re.match(r"test_", file):
#                 check(os.path.join(path, file))


# def check(path):
#     with open(f"{path}", "r") as file:
#         lines = file.readlines()
#         code_lines = [
#             CodeLine(i, line, lines)
#             for i, line in enumerate(lines)
#         ]

#     # Run all checks:
#     errors = [
#         error_message(c, f.__name__, desc, f(c), path)
#         for c in code_lines
#         for f, desc in ERR_DESCS.items()
#     ]

#     # Throw out all non-errors and print
#     errors = list(filter(None, errors))
#     for e in errors:
#         print(e)


# def error_message(c: CodeLine, name: str, desc: str, failed: bool, file: str):
#     if failed:
#         return f'{file}: Line {c.ln_num + 1}: {name} {desc}'
#     return None


# if __name__ == '__main__':
#     main()



