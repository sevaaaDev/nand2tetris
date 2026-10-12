from typing import Callable

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
        if type(r) == str:
            if r != text[i]:
                return None
            i+=1
        if callable(r):
           i += r(capture_arr, text[i:])
    return capture_arr

def macro_expand(text: str) -> list[str]:
    captured = capture(text, ["D", "=", "M", "[", cpt(lambda c: c != "]"), "]"])
    if captured is not None:
        return [f"@{captured[0]}", "D=M"]
    return [text]
