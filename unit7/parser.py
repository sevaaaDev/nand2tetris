import tokens
from lexer import Lexer

def parse_push(lex: Lexer):
    segment = ""
    digit = ""
    tok = lex.peek()
    if tok[0] != tokens.PUSH:
        raise SyntaxError(f"expected 'push', got '{tok[1]}'")
    lex.eat()

    tok = lex.peek()
    if tok[0] != tokens.SEGMENT:
        raise SyntaxError(f"expected SEGMENT, got '{tok[1]}'")
    segment = lex.eat()[1]

    tok = lex.peek()
    if tok[0] != tokens.DIGIT:
        raise SyntaxError(f"expected DIGIT, got '{tok[1]}'")
    digit = lex.eat()[1]
    return PushCommand(segment, digit)

def parse_pop(lex: Lexer):
    segment = ""
    digit = ""
    tok = lex.peek()
    if tok[0] != tokens.POP:
        raise SyntaxError(f"expected 'push', got '{tok[1]}'")
    lex.eat()

    tok = lex.peek()
    if tok[0] != tokens.SEGMENT:
        raise SyntaxError(f"expected SEGMENT, got '{tok[1]}'")
    segment = lex.eat()[1]

    tok = lex.peek()
    if tok[0] != tokens.DIGIT:
        raise SyntaxError(f"expected DIGIT, got '{tok[1]}'")
    digit = lex.eat()[1]
    return PopCommand(segment, digit)

def parse_arith(lex: Lexer):
    tok = lex.peek()
    if tok[0] != tokens.ARITHMETIC:
        raise SyntaxError(f"expected arithmetic command, got '{tok[1]}'")
    return ArithmeticCommand(lex.eat()[1])

def parse(lex: Lexer):
    tok = lex.peek()
    match tok[0]:
        case tokens.PUSH:
            return parse_push(lex)
        case tokens.POP:
            return parse_pop(lex)
        case tokens.ARITHMETIC:
            return parse_arith(lex)
