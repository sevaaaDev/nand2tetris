from lexer import Lexer, Scanner
from parser import parse
from command import FuncCommand, PushCommand

def test_parsing_function():
    filestr = """function Foo.bar 1
    push constant 17
    pop local 0
    """
    lex = Lexer(Scanner(filestr))
    cmd = parse(lex)
    assert isinstance(cmd, FuncCommand)
    assert len(cmd.body) == 2

def test_parsing_function_return():
    filestr = """function Foo.bar 1
    push constant 17
    pop local 0
    return
    push constant 2
    """
    lex = Lexer(Scanner(filestr))
    cmd = parse(lex)
    assert isinstance(cmd, FuncCommand)
    assert len(cmd.body) == 3
    cmd = parse(lex)
    assert isinstance(cmd, PushCommand)
