from lexer import Lexer
from parser import Parser
def main():
    filestr = """class Foo {
    static int bar, baz, quma;
    static char doof, moo, lom;
    method void foo(int a, int b, char c) {
        var int damar, woomp;
        return 1;
    }
    method void foo(int a, int b, char c) {
        return 1;
    }
    method void foo(int a, int b, char c) {
        var int damar;
        var char moora;
    }
    """
    lex = Lexer(filestr)
    parse = Parser(lex)
    try:
        parse.main()
    except SyntaxError as e:
        print(e)

main()
