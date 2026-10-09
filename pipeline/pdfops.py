"""Per-paint-operator control over a PDF page content stream.

The page stream is tokenized once. Every painting operator (path fill/stroke,
text show, XObject Do, shading sh, inline image) gets an index. `render_subset`
rebuilds the stream so that only the chosen painting operators draw, while every
state operator (cm, gs, clip, colors, text positioning) is kept untouched, so
the kept objects render exactly where and how they render in the full page.
"""
import re

DELIM = b"()<>[]{}/%"
WS = b" \t\r\n\f\x00"
PATH_PAINT = {b"f", b"F", b"f*", b"S", b"s", b"B", b"B*", b"b", b"b*"}
TEXT_SHOW = {b"Tj", b"TJ", b"'", b'"'}
OTHER_PAINT = {b"Do", b"sh", b"BI"}
NUM = re.compile(rb"[+-]?(\d+\.?\d*|\.\d+)")


def tokenize(data):
    i, n = 0, len(data)
    while i < n:
        c = data[i:i + 1]
        if c in WS:
            i += 1
            continue
        if c == b"%":
            while i < n and data[i:i + 1] not in b"\r\n":
                i += 1
            continue
        s = i
        if c == b"(":
            depth = 0
            while i < n:
                ch = data[i:i + 1]
                if ch == b"\\":
                    i += 2
                    continue
                if ch == b"(":
                    depth += 1
                elif ch == b")":
                    depth -= 1
                    if depth == 0:
                        i += 1
                        break
                i += 1
            yield s, i, "operand", None
            continue
        if c == b"<":
            if data[i:i + 2] == b"<<":
                i += 2
                yield s, i, "operand", b"<<"
                continue
            i = data.index(b">", i) + 1
            yield s, i, "operand", None
            continue
        if c == b">" and data[i:i + 2] == b">>":
            i += 2
            yield s, i, "operand", b">>"
            continue
        if c in b"[]{}":
            i += 1
            yield s, i, "operand", c
            continue
        if c == b"/":
            i += 1
            while i < n and data[i:i + 1] not in WS and data[i:i + 1] not in DELIM:
                i += 1
            yield s, i, "operand", None
            continue
        while i < n and data[i:i + 1] not in WS and data[i:i + 1] not in DELIM:
            i += 1
        word = data[s:i]
        if NUM.fullmatch(word) or word in (b"true", b"false", b"null"):
            yield s, i, "operand", None
            continue
        if word == b"BI":
            m = re.compile(rb"\sEI(?=\s|$)").search(data, i)
            i = m.end()
            yield s, i, "op", b"BI"
            continue
        yield s, i, "op", word


class PageOps:
    def __init__(self, data):
        self.data = data
        # list of (op, start_of_operands, end)
        self.ops = []
        seg = 0
        for s, e, kind, val in tokenize(data):
            if kind == "op":
                self.ops.append((val, seg, e))
                seg = e
        self.paint = [k for k, (op, _, _) in enumerate(self.ops)
                      if op in PATH_PAINT or op in TEXT_SHOW or op in OTHER_PAINT]

    def __len__(self):
        return len(self.paint)

    def render_subset(self, keep):
        """keep: set of paint indices to draw."""
        keep_ops = {self.paint[i] for i in keep}
        paint_set = set(self.paint)
        out = []
        tr = b"0"  # current text render mode as written in stream
        tr_stack = []
        for k, (op, s, e) in enumerate(self.ops):
            chunk = self.data[s:e]
            if op == b"q":
                tr_stack.append(tr)
            elif op == b"Q":
                tr = tr_stack.pop() if tr_stack else b"0"
            elif op == b"Tr":
                tr = chunk.split()[-2]
            if k in paint_set and k not in keep_ops:
                if op in PATH_PAINT:
                    out.append(b" n")
                elif op in TEXT_SHOW:
                    # draw invisibly so the text cursor still advances
                    out.append(b" 3 Tr" + chunk + b" " + tr + b" Tr")
                else:
                    out.append(b" ")
                continue
            out.append(chunk)
        return b"".join(out)
