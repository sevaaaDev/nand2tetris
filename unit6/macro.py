from typing import Callable

class Rules():
    @staticmethod
    def cpt(fn: Callable[[str], bool]) -> CaptureFunc:
        def capture_this(capture_arr: list[str], text: str) -> int:
            addr: str = ""
            i: int = 0
            for c in text:
                if not fn(c):
                    break
                addr+=c
                i+=1
            capture_arr.append(addr)
            return i
        return capture_this

    @staticmethod
    def any_until(char: str) -> CaptureFunc:
        return Rules.cpt(lambda c: c != char)

type CaptureFunc = Callable[[list[str], str], int]
type RulesType = list[str | CaptureFunc]
def capture(text: str, rules: RulesType) -> list[str] | None:
    # WARN: here we dont check the len of the text
    # we could have abc32, with rules "abc" and still pass
    # but, 32abc doesnt pass

    # TODO: implemnet func non capture .* | [abc]
    # TODO: implemnet func compare word (ab | bc | cd)
    capture_arr: list[str] = []
    i = 0
    for r in rules:
        if i >= len(text):
            return None
        if type(r) == str:
            if r != text[i]:
                return None
            i+=1
        if callable(r):
           i += r(capture_arr, text[i:])
    if i != len(text):
        return None
    return capture_arr

def macro_expand(text: str) -> list[str]:
    captured = capture(text, [*"D=M[", Rules.any_until("]"), "]", ";", Rules.any_until("")])
    if captured is not None:
        return [f"@{captured[0]}", f"D=M;{captured[1]}"]
    # BUG: below rules is too forgiving
    ## captured = capture(text, [Rules.any_until(";"), ";", Rules.any_until(" "), " ", Rules.any_until("")])
    if captured is not None:
        return [f"@{captured[2]}", f"{captured[0]};{captured[1]}"]
    captured = capture(text, [*"M[", Rules.any_until("]"), *"]=", Rules.any_until("")])
    if captured is not None:
        return [f"@{captured[0]}", f"M={captured[1]}"]
    return [text]

# print(macro_expand("D=M[hello]"))
# print(macro_expand("D;JGT label"))
# print(macro_expand("D;JGT"))
# print(macro_expand("D=M;JGT"))
