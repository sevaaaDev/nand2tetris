def main():
    filestr = "if (x) {}"
    lex = Lexer(filestr)
    parser.main(lex)
