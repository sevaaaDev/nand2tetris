from lexer import Lexer
import token

class OutputWriter:
    def __init__(self):
        self._indent = 0

    def print(self, text):
        print("\t" * self._indent + str(text))
    def indent(self):
        self._indent += 1

    def deindent(self):
        self._indent -= 1

class Parser:
    TYPE = (token.INT, token.CHAR, token.BOOLEAN, token.IDENTIFIER)
    OP = (token.PLUS, token.MINUS, token.STAR, token.SLASH, token.AMPERSAND, token.PIPE, token.LESS, token.GREATER, token.EQUAL)
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
        self.expectRule(self.jack_class, "expecting a class definition")

    def jack_class(self):
        if not self.check(token.CLASS):
            return
        self.eat()
        self.owriter.print("class")
        self.expect(token.IDENTIFIER)
        self.expect(token.LEFT_BRACE)
        self.owriter.indent()
        self.jack_classVarDec()
        self.jack_subroutineDec()
        self.owriter.deindent()
        return True

    def jack_classVarDec(self):
        if not self.check(token.STATIC, token.FIELD):
            return
        self.owriter.print("class var declaration")
        while self.check(token.STATIC, token.FIELD):
            self.eat()
            self._var_dec()
            self.expect(token.SEMICOLON)
        return True

    def jack_subroutineDec(self):
        if not self.check(token.CONSTRUCTOR, token.METHOD, token.FUNCTION):
            return
        self.owriter.print("subroutine declaration")
        while self.check(token.CONSTRUCTOR, token.METHOD, token.FUNCTION):
            self.eat()
            self.expect(*Parser.TYPE, token.VOID)
            self.expect(token.IDENTIFIER)
            self.expect(token.LEFT_PAREN)
            self.owriter.indent()
            self.jack_paramList()
            self.owriter.deindent()
            self.expect(token.RIGHT_PAREN)
            self.owriter.indent()
            self.expectRule(self.jack_subroutineBody, "expecting subroutine body")
            self.owriter.deindent()
        return True

    def jack_subroutineBody(self):
        if not self.check(token.LEFT_BRACE):
            return
        self.eat()
        self.owriter.print("subroutine body")
        while self.check(token.VAR):
            self.eat()
            self._var_dec()
            self.expect(token.SEMICOLON)
        self.jack_statements()
        self.expect(token.RIGHT_BRACE)
        return True

    def _var_dec(self):
        self.expect(*Parser.TYPE)
        self.expect(token.IDENTIFIER)
        while self.check(token.COMMA):
            self.eat()
            self.expect(token.IDENTIFIER)
            self.eat()

    def jack_paramList(self):
        if not self.check(*Parser.TYPE):
            return
        self.owriter.print("param list")
        self.eat()
        self.expect(token.IDENTIFIER)
        while self.check(token.COMMA):
            self.eat()
            self.expect(*Parser.TYPE)
            self.expect(token.IDENTIFIER)
        return True

    def jack_statements(self):
        # if not self.check(token.LET, token.IF, token.WHILE, token.DO, token.RETURN):
        #     return
        self.owriter.print("statements")
        self.owriter.indent()
        while self.jack_let() or self.jack_if() or self.jack_while() or self.jack_do() or self.jack_return():
            pass
        self.owriter.deindent()
        # while self.check(token.LET, token.IF, token.WHILE, token.DO, token.RETURN):
        #     tok = self.peek()[0]
        #     self.eat()
        #     match tok:
        #         case t if t == token.LET:
        #             self.jack_let()
        #         case t if t == token.IF:
        #             self.jack_if()
        #         case t if t == token.WHILE:
        #             self.jack_while()
        #         case t if t == token.DO:
        #             self.jack_do()
        #         case t if t == token.RETURN:
        #             self.jack_return()

    def jack_let(self):
        if not self.check(token.LET):
            return
        self.eat()
        self.owriter.print("let")
        self.expect(token.IDENTIFIER)
        if self.check(token.LEFT_BRACKET):
            self.expectRule(self.jack_expr, "expecting expression")
            self.expect(token.RIGHT_BRACKET)
        self.expect(token.EQUAL)
        self.expectRule(self.jack_expr, "expecting expression")
        self.expect(token.SEMICOLON)
        return True

    def jack_if(self):
        if not self.check(token.IF):
            return
        self.eat()
        self.owriter.print("if")
        self.expect(token.LEFT_PAREN)
        self.expectRule(self.jack_expr, "expecting expression")
        self.expect(token.RIGHT_PAREN)
        self.expect(token.LEFT_BRACE)
        self.expectRule(self.jack_statements, "expecting statements")
        self.expect(token.RIGHT_BRACE)
        self.expectRule(self.jack_statements, "expecting statements")
        if self.check(token.ELSE):
            self.eat()
            self.expect(token.LEFT_BRACE)
            self.expectRule(self.jack_statements, "expecting statements")
            self.expect(token.RIGHT_BRACE)
        return True

    def jack_while(self):
        if not self.check(token.WHILE):
            return
        self.eat()
        self.owriter.print("while")
        self.expect(token.LEFT_PAREN)
        self.expectRule(self.jack_expr, "expecting expression")
        self.expect(token.RIGHT_PAREN)
        self.expect(token.LEFT_BRACE)
        self.expectRule(self.jack_statements, "expecting statements")
        self.expect(token.RIGHT_BRACE)
        self.expectRule(self.jack_statements, "expecting statements")
        return True

    def jack_do(self):
        if not self.check(token.DO):
            return
        self.eat()
        self.owriter.print("do")
        self.expectRule(self.jack_subroutineCall, "expecting subroutine call")
        self.expect(token.SEMICOLON)
        return True

    def jack_return(self):
        if not self.check(token.RETURN):
            return
        self.eat()
        self.owriter.print("return")
        self.jack_expr()
        self.expect(token.SEMICOLON)
        return True

    def jack_subroutineCall(self):
        if not self.check(token.IDENTIFIER):
            return
        self.eat()
        if self.check(token.DOT):
            self.eat()
            self.expect(token.IDENTIFIER)
        self.expect(token.LEFT_PAREN)
        self.jack_exprList()
        self.expect(token.RIGHT_PAREN)
        return True

    def jack_exprList(self):
        if self.jack_expr() is None:
            return
        while self.check(token.COMMA):
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
        if self.check(token.INTEGER):
            pass
        if self.check(token.STRING):
            pass
        if self.check(token.TRUE):
            pass
        if self.check(token.FALSE):
            pass
        if self.check(token.NULL):
            pass
        if self.check(token.THIS):
            pass
        if self.check(token.IDENTIFIER):
            self.eat()
            if self.check(token.LEFT_BRACKET):
                self.expectRule(self.jack_expr, "expecting expression")
                self.expect(token.RIGHT_BRACKET)
        if self.jack_subroutineCall():
            pass
        if self.check(token.LEFT_PAREN):
            self.eat()
            self.expectRule(self.jack_expr, "expecting expression")
            self.expect(token.RIGHT_PAREN)
        if self.check(token.MINUS) or self.check(token.NEGATE):
            self.eat()
            self.expectRule(self.jack_term, "expecting expression")
        self.eat()
        return True

