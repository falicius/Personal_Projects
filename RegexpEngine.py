reg, str = input().split("|")


def compare_chr(reg, str) -> bool:
    return reg == str or bool(reg == "." and str) or not reg


def compare(reg, str) -> bool:
    if not reg or (reg == "$" and not str):
        return True
    if not str:
        return False
    if len(reg) > 1 and reg[1] == "?" and reg[0] != "\\":
        return compare(reg[2:], str) or compare(reg[2:], str[1:])
    if len(reg) > 1 and reg[1] == "*" and reg[0] != "\\":
        return compare(reg[2:], str) or compare(reg, str[1:])
    if len(reg) > 1 and reg[1] == "+" and reg[0] != "\\":
        return compare(reg.replace('+', '*', 1), str[1:])
    if len(reg) > 1 and reg[0] == "\\":
        return compare(reg[1:], str)
    if compare_chr(reg[0], str[0]):
        return compare(reg[1:], str[1:])
    return False


def regex(reg, str) -> bool:
    if not reg:
        return True
    if not str:
        return False
    if reg[0] == '^':
        return compare(reg[1:], str)
    if compare(reg, str):
        return True
    return regex(reg, str[1:])


print(regex(reg, str))
