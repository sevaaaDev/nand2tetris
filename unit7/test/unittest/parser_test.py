from lexer import MOCK_Lexer
from parser import parse
import tokens
import pytest

def test_parser_normal_input():
    lex = MOCK_Lexer([(tokens.PUSH, "push"), (tokens.SEGMENT, "constant"), (tokens.DIGIT, "17")])
    cmd = parse(lex)
    assert cmd.to_asm() == "// push constant 17"

def test_parser_bad_input():
    lex = MOCK_Lexer([(tokens.PUSH, "push"), (tokens.DIGIT, "17")])
    with pytest.raises(SyntaxError):
        parse(lex)

def test_parser_no_input():
    lex = MOCK_Lexer([])
    with pytest.raises(SyntaxError):
        parse(lex)


