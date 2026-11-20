from parser import Parser
from lexer import Lexer
import pytest

def test_term():
    print("=== test_term ===")
    terms = ["1", "foo", "null", "this", "false", "true", "(5 + 10)", "foo[1]", "foo[(5 + 10)]", "foo.bar()", "bar()", "-1", "~true"]
    for t in terms:
        print(f"TEST: {t}", end="")
        l = Lexer(t)
        p = Parser(l)
        p.jack_term()
        print(f"\r\033[KOK: {t}")

def test_expr():
    print("=== test_expr ===")
    expr = ["5 + 10", "foo", "5", "(5 + 10) * 2"]
    for e in expr:
        print(f"TEST: {e}", end="")
        l = Lexer(e)
        p = Parser(l)
        p.jack_term()
        print(f"\r\033[KOK: {e}")

def test_class():
    classstr = """
    class Foo {
        field int x, y;
        static int SIZE;
        function void init(int size) {
            var int i;
            let SIZE = size;
            do bar.init();
            while (false) {
                let i = i + 1;
            }
        }
        constructor Foo new(int _x, int _y) {
            let x = _x;
            let y = _y;
            return this;
        }
        method int getX() {
            return x;
        }
        method int getY() {
            return y;
        }
        method void move(int dx, int dy) {
            let x = x+dx;
            let y = y+dy;
        }
        method boolean isOutside() {
            if ((x > SIZE) | (x < 0) | (y > SIZE) | (y < 0)) {
                return true;
            } else {
                return false;
            }
        }
    }
    """
    l = Lexer(classstr)
    p = Parser(l)
    p.main()

def test_if():
    success = ["""
    if ((5 * 2) < 10) {
        return 1;
    }
    """, """
    if ((5 * 2) < 10) {
        return 1;
    } else {
        return 2;
    }
    """, """
    if ((5 * 2) < 10) {
        do Output.print("Yessss");
        return 1;
    } else {
        return 2;
    }
    """]
    error = ["""
    if ((5 * 2) < 10) {
    }
    """, """
    if ((5 * 2) < 10) {
        return 1;
    } else {
    }
    """, """
    if ((5 * 2) < 10) {
    } else {
    }
    """, """
    if () {
        return 1;
    } 
    """]
    for s in success:
        l = Lexer(s)
        p = Parser(l)
        assert True == p.jack_if()
    for e in error:
        l = Lexer(e)
        p = Parser(l)
        with pytest.raises(SyntaxError):
            p.jack_if()

def test_while():
    success = ["while (true) {return 1;}", "while (true) {do foo.bar(); return 1;}"]
    error = ["while (true) {}", "while () {}"]
    for s in success:
        l = Lexer(s)
        p = Parser(l)
        assert True == p.jack_while()
    for e in error:
        l = Lexer(e)
        p = Parser(l)
        with pytest.raises(SyntaxError):
            p.jack_while()

def test_return():
    success = ["return;", "return (3+2);"]
    error = ["return"]
    for s in success:
        l = Lexer(s)
        p = Parser(l)
        assert True == p.jack_return()
    for e in error:
        l = Lexer(e)
        p = Parser(l)
        with pytest.raises(SyntaxError):
            p.jack_return()

def test_do():
    success = ["do foo();", "do foo.bar();", "do foo(3+1);"]
    error = ["do foo()", "do foo.();"]
    for s in success:
        l = Lexer(s)
        p = Parser(l)
        assert True == p.jack_do()
    for e in error:
        l = Lexer(e)
        p = Parser(l)
        with pytest.raises(SyntaxError):
            p.jack_do()

def test_let():
    success = ["let foo = 1;", "let foo[3] = foo[2];"]
    error = ["let foo = 1", "let foo[] = 3;"]
    for s in success:
        l = Lexer(s)
        p = Parser(l)
        assert True == p.jack_let()
    for e in error:
        l = Lexer(e)
        p = Parser(l)
        with pytest.raises(SyntaxError):
            p.jack_let()

def test_subroutine():
    sub = """
    method int foo(int y) {
        var int i;
        var int k;
        while (i < y) {
            let k = k+i;
        }
        return k;
    }
    function int foo(int y) {
        var int i;
        var int k;
        while (i < y) {
            let k = k+i;
        }
        return k;
    }
    """
    l = Lexer(sub)
    p = Parser(l)
    assert True == p.jack_subroutineDec()
