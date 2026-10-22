import tokens
import sys
from parser import parse
from lexer import MOCK_Lexer

# TODO: test parser
# TODO: implement lexer
# TODO: implement to_asm()
MOCK_LINES = [
    [(tokens.PUSH, "push"), (tokens.SEGMENT, "constant"), (tokens.DIGIT, "17")],
    [(tokens.PUSH, "push"), (tokens.DIGIT, "constant"), (tokens.DIGIT, "10")],
    [(tokens.ARITHMETIC, "add")],
    [(tokens.POP, "pop"), (tokens.SEGMENT, "constant"), (tokens.DIGIT, "0")],
]

def main() -> None:
    # TODO: handle line num and comment
    cmds = []
    err = False
    for tokens in MOCK_LINES:
        lexer = MOCK_Lexer(tokens)
        try:
            cmd = parse(lexer)
            cmds.append(cmd)
        except Exception as e:
            print(f"syntax error: {str(e)}", file=sys.stderr)
    for c in cmds:
        try:
            c.semantic_check()
        except Exception as e:
            print(f"semantic error: {str(e)}", file=sys.stderr)
            err = True
    if err:
        sys.exit(1)
    for c in cmds:
        print(c.to_asm())

main()
