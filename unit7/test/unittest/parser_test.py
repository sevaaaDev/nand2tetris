from lexer import MOCK_Lexer
from parser import parse
import command
import tokens
import pytest

def test_parser_normal_input():
    lex = MOCK_Lexer([(tokens.PUSH, "push"), (tokens.SEGMENT, "constant"), (tokens.DIGIT, "17")])
    cmd = parse(lex)
    assert isinstance(cmd, command.PushCommand)

def test_parser_bad_input():
    lex = MOCK_Lexer([(tokens.PUSH, "push"), (tokens.DIGIT, "17")])
    with pytest.raises(SyntaxError):
        parse(lex)

def test_parser_no_input():
    lex = MOCK_Lexer([])
    with pytest.raises(SyntaxError):
        parse(lex)

def test_parse_function():
    lex = MOCK_Lexer([(tokens.FUNC, "function"), (tokens.IDENT, "Foo.bar"), (tokens.DIGIT, "2")])
    cmd = parse(lex)
    assert isinstance(cmd, command.FuncCommand)

def test_parse_invalid_function():
    lex = MOCK_Lexer([(tokens.FUNC, "function"), (tokens.IDENT, "Foo.bar")])
    with pytest.raises(SyntaxError):
        parse(lex)
