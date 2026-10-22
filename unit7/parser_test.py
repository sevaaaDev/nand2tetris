from lexer import MOCK_Lexer
from parser import parse

def test():
    lex = MOCK_Lexer([(tokens.PUSH, "push"), (tokens.SEGMENT, "constant"), (tokens.DIGIT, "17")])
    cmd = parse(lex)
    assert cmd.to_asm() == "// push constant 17"

