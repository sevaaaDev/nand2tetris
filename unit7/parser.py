import tokens
from lexer import Lexer
from command import Command, PushCommand, PopCommand, ArithmeticCommand

PUSH_RULES = (PushCommand, [tokens.PUSH, tokens.SEGMENT, tokens.DIGIT])
POP_RULES = (PopCommand, [tokens.POP, tokens.SEGMENT, tokens.DIGIT])
ARITH_RULES = (ArithmeticCommand, [tokens.ARITHMETIC])
def parse_cmd(lex: Lexer, rules: tuple[type[Command], list[str]]) -> Command:
    data: list[str] = []
    for r in rules[1]:
        tok = lex.peek()
        if tok is None:
            raise SyntaxError(f"expected {r}, got nothing")
        if tok[0] != r:
            raise SyntaxError(f"expected {r}, got '{tok[0]}'")
        lex.eat()
        data.append(tok[1])
    if lex.peek() is not None:
        raise SyntaxError(f"expected newline, got something else")
    return rules[0](data)
    
# def parse_push(lex: Lexer) -> Command:
#     segment = ""
#     digit = ""
#     tok = lex.peek()
#     if tok[0] != tokens.PUSH:
#         raise SyntaxError(f"expected 'push', got '{tok[1]}'")
#     lex.eat()

#     tok = lex.peek()
#     if tok[0] != tokens.SEGMENT:
#         raise SyntaxError(f"expected SEGMENT, got '{tok[1]}'")
#     segment = lex.eat()[1]

#     tok = lex.peek()
#     if tok[0] != tokens.DIGIT:
#         raise SyntaxError(f"expected DIGIT, got '{tok[1]}'")
#     digit = lex.eat()[1]
#     return PushCommand(segment, digit)

# def parse_pop(lex: Lexer):
#     segment = ""
#     digit = ""
#     tok = lex.peek()
#     if tok[0] != tokens.POP:
#         raise SyntaxError(f"expected 'push', got '{tok[1]}'")
#     lex.eat()

#     tok = lex.peek()
#     if tok[0] != tokens.SEGMENT:
#         raise SyntaxError(f"expected SEGMENT, got '{tok[1]}'")
#     segment = lex.eat()[1]

#     tok = lex.peek()
#     if tok[0] != tokens.DIGIT:
#         raise SyntaxError(f"expected DIGIT, got '{tok[1]}'")
#     digit = lex.eat()[1]
#     return PopCommand(segment, digit)

# def parse_arith(lex: Lexer):
#     tok = lex.peek()
#     if tok[0] != tokens.ARITHMETIC:
#         raise SyntaxError(f"expected arithmetic command, got '{tok[1]}'")
#     return ArithmeticCommand(lex.eat()[1])

def parse(lex: Lexer) -> Command:
    tok = lex.peek()
    if tok is None:
        raise SyntaxError("expecting")
    match tok[0]:
        case tokens.PUSH:
            return parse_cmd(lex, PUSH_RULES)
        case tokens.POP:
            return parse_cmd(lex, POP_RULES)
        case tokens.ARITHMETIC:
            return parse_cmd(lex, ARITH_RULES)
        case _:
            raise SyntaxError(f"this should not happen: {tok[0]} fail to match any rules")
