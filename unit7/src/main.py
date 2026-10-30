import tokens
import sys
from pathlib import Path
from parser import parse
from lexer import Lexer, Scanner
from command import SemanticError

# TODO: implement to_asm()

def error(msg: str, filename: str, linenum: int, line: str):
    print(f"{filename}:{linenum}: {msg}", file=sys.stderr)
    print(f"in expression:", file=sys.stderr)
    print(f"\t{line}", file=sys.stderr)

def translate(filename: str):
    cmds = []
    err = False
    linenum = 0
    with open(filename) as f:
        filestr = f.read()
        lexer = Lexer(Scanner(filestr))
        while True:
            try:
                cmd = parse(lexer)
                cmd.semantic_check()
                cmds.append(cmd)
            except EOFError as e:
                break
            except SyntaxError as e:
                error(f"syntax error: {str(e)}", filename, lexer.linenum, lexer.line)
                err = True
            except SemanticError as e:
                error(f"semantic error: {str(e)}", filename, lexer.linenum, lexer.line)
                err = True
    if err:
        sys.exit(1)
    for c in cmds:
        print(c.to_asm(Path(filename).stem))
    
def main() -> None:
    if len(sys.argv) < 2:
        print(f"{sys.argv[0]}: missing filename", file=sys.stderr)
        print(f"Example:", file=sys.stderr)
        print(f"\tpython {sys.argv[0]} filename.vm", file=sys.stderr)
        sys.exit(1)
    filename = sys.argv[1]
    translate(filename)

main()
