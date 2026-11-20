from lexer import Lexer
import tokens

class OutputWriter:
    def __init__(self):
        self._indent = 0

    def print(self, text):
        # print("\t" * self._indent + str(text))
        pass
    def indent(self):
        self._indent += 1

    def deindent(self):
        self._indent -= 1

class Parser:
    TYPE = (tokens.INT, tokens.CHAR, tokens.BOOLEAN, tokens.IDENTIFIER)
    OP = (tokens.PLUS, tokens.MINUS, tokens.STAR, tokens.SLASH, tokens.AMPERSAND, tokens.PIPE, tokens.LESS, tokens.GREATER, tokens.EQUAL)
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.lastToken = None
        self.owriter = OutputWriter()

    def peek(self):
        if self.lastToken is None:
            self.lastToken = self.lexer.lex()
        return self.lastToken

    def eat(self):
        self.lastToken = None

    def check(self, *tok: str):
        for t in tok:
            if self.peek()[0] == t:
                return True
        return False

    def expect(self, *tok: str) -> str:
        if not self.check(*tok):
            raise SyntaxError(f"expecting: {tok}, got: {self.lastToken[1]}")
        newTok = self.peek()
        self.eat()
        # self.owriter.print(newTok)
        return newTok

    def expectRule(self, rule, msg):
        res = rule()
        if res is None:
            raise SyntaxError(msg)
        return res

    def main(self):
        return self.expectRule(self.jack_class, "expecting a class definition")

    def jack_class(self):
        if not self.check(tokens.CLASS):
            return
        self.eat()
        self.owriter.print("class")
        self.expect(tokens.IDENTIFIER)
        self.expect(tokens.LEFT_BRACE)
        self.owriter.indent()
        self.jack_classVarDec()
        self.jack_subroutineDec()
        self.owriter.deindent()
        return True

    def jack_classVarDec(self):
        if not self.check(tokens.STATIC, tokens.FIELD):
            return
        self.owriter.print("class var declaration")
        while self.check(tokens.STATIC, tokens.FIELD):
            self.eat()
            self._var_dec()
            self.expect(tokens.SEMICOLON)
        return True

    def jack_subroutineDec(self):
        if not self.check(tokens.CONSTRUCTOR, tokens.METHOD, tokens.FUNCTION):
            return
        self.owriter.print("subroutine declaration")
        while self.check(tokens.CONSTRUCTOR, tokens.METHOD, tokens.FUNCTION):
            self.eat()
            self.expect(*Parser.TYPE, tokens.VOID)
            self.expect(tokens.IDENTIFIER)
            self.expect(tokens.LEFT_PAREN)
            self.owriter.indent()
            self.jack_paramList()
            self.owriter.deindent()
            self.expect(tokens.RIGHT_PAREN)
            self.owriter.indent()
            self.expectRule(self.jack_subroutineBody, "expecting subroutine body")
            self.owriter.deindent()
        return True

    def jack_subroutineBody(self):
        if not self.check(tokens.LEFT_BRACE):
            return
        self.eat()
        self.owriter.print("subroutine body")
        while self.check(tokens.VAR):
            self.eat()
            self._var_dec()
            self.expect(tokens.SEMICOLON)
        self.jack_statements()
        self.expect(tokens.RIGHT_BRACE)
        return True

    def _var_dec(self):
        self.expect(*Parser.TYPE)
        self.expect(tokens.IDENTIFIER)
        while self.check(tokens.COMMA):
            self.eat()
            self.expect(tokens.IDENTIFIER)
            self.eat()

    def jack_paramList(self):
        if not self.check(*Parser.TYPE):
            return
        self.owriter.print("param list")
        self.eat()
        self.expect(tokens.IDENTIFIER)
        while self.check(tokens.COMMA):
            self.eat()
            self.expect(*Parser.TYPE)
            self.expect(tokens.IDENTIFIER)
        return True

    def jack_statements(self):
        # if not self.check(tokens.LET, tokens.IF, tokens.WHILE, tokens.DO, tokens.RETURN):
        #     return
        if (self.jack_let() or self.jack_if() or self.jack_while() or self.jack_do() or self.jack_return()) is None:
            return
        self.owriter.print("statements")
        self.owriter.indent()
        while self.jack_let() or self.jack_if() or self.jack_while() or self.jack_do() or self.jack_return():
            pass
        self.owriter.deindent()
        return True

    def jack_let(self):
        if not self.check(tokens.LET):
            return
        self.eat()
        self.owriter.print("let")
        self.expect(tokens.IDENTIFIER)
        if self.check(tokens.LEFT_BRACKET):
            self.eat();
            self.expectRule(self.jack_expr, "expecting expression")
            self.expect(tokens.RIGHT_BRACKET)
        self.expect(tokens.EQUAL)
        self.expectRule(self.jack_expr, "expecting expression")
        self.expect(tokens.SEMICOLON)
        return True

    def jack_if(self):
        if not self.check(tokens.IF):
            return
        self.eat()
        self.owriter.print("if")
        self.expect(tokens.LEFT_PAREN)
        self.expectRule(self.jack_expr, "expecting expression")
        self.expect(tokens.RIGHT_PAREN)
        self.expect(tokens.LEFT_BRACE)
        self.expectRule(self.jack_statements, "expecting statements")
        self.expect(tokens.RIGHT_BRACE)
        if self.check(tokens.ELSE):
            self.eat()
            self.expect(tokens.LEFT_BRACE)
            self.expectRule(self.jack_statements, "expecting statements")
            self.expect(tokens.RIGHT_BRACE)
        return True

    def jack_while(self):
        if not self.check(tokens.WHILE):
            return
        self.eat()
        self.owriter.print("while")
        self.expect(tokens.LEFT_PAREN)
        self.expectRule(self.jack_expr, "expecting expression")
        self.expect(tokens.RIGHT_PAREN)
        self.expect(tokens.LEFT_BRACE)
        self.expectRule(self.jack_statements, "expecting statements")
        self.expect(tokens.RIGHT_BRACE)
        return True

    def jack_do(self):
        if not self.check(tokens.DO):
            return
        self.eat()
        self.owriter.print("do")
        self.expectRule(self.jack_subroutineCall, "expecting subroutine call")
        self.expect(tokens.SEMICOLON)
        return True

    def jack_return(self):
        if not self.check(tokens.RETURN):
            return
        self.eat()
        self.owriter.print("return")
        self.jack_expr()
        self.expect(tokens.SEMICOLON)
        return True

    def jack_subroutineCall(self):
        if not self.check(tokens.IDENTIFIER):
            return
        self.eat()
        if self.check(tokens.DOT):
            self.eat()
            self.expect(tokens.IDENTIFIER)
        self.expect(tokens.LEFT_PAREN)
        self.jack_exprList()
        self.expect(tokens.RIGHT_PAREN)
        return True

    def jack_exprList(self):
        if self.jack_expr() is None:
            return
        while self.check(tokens.COMMA):
            self.eat()
            self.expectRule(self.jack_expr, "expecting expression")
        return True

    def jack_expr(self):
        self.owriter.print("expression")
        self.owriter.indent()
        if self.jack_term() is None:
            return
        while self.check(*Parser.OP):
            self.eat()
            self.expectRule(self.jack_term, "expecting expression")
        self.owriter.deindent()
        return True

    def jack_term(self):
        # TODO: this is wrong, if no match must return none
        self.owriter.print("term")
        if self.check(tokens.INTEGER):
            self.eat()
            return True
        if self.check(tokens.STRING):
            self.eat()
            return True
        if self.check(tokens.TRUE):
            self.eat()
            return True
        if self.check(tokens.FALSE):
            self.eat()
            return True
        if self.check(tokens.NULL):
            self.eat()
            return True
        if self.check(tokens.THIS):
            self.eat()
            return True
        if self.check(tokens.IDENTIFIER):
            self.eat()
            if self.check(tokens.LEFT_BRACKET):
                self.eat()
                self.expectRule(self.jack_expr, "expecting expression")
                self.expect(tokens.RIGHT_BRACKET)
            return True
        if self.jack_subroutineCall():
            return True
        if self.check(tokens.LEFT_PAREN):
            self.eat()
            self.expectRule(self.jack_expr, "expecting expression")
            self.expect(tokens.RIGHT_PAREN)
            return True
        if self.check(tokens.MINUS) or self.check(tokens.NEGATE):
            self.eat()
            self.expectRule(self.jack_term, "expecting expression")
            return True
        return 

