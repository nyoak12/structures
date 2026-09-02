import re
from pprint import pprint


# the + means one or more tokens open for whitespace
# \d means any zero or more digits
# \ means followed by
#
patterns = [
    (r"\s+", "whitespace"),
    (r"\d*\.\d+|\d+\.\d*|\d+", "number"),
    (r"\+", "+"),
    (r"\-", "-"),
    (r"\/", "/"),
    (r"\*", "*"),
    (r"\(", "("),
    (r"\)", ")"),
    (r".", "error"), # "." this means anything
]

#list comprehension
# replaces regex with compiled version -> re.compile
patterns = [(re.compile(p), tag) for p, tag in patterns]

def tokenize(characters):
    "Tokenize a string using the patterns above"
    tokens = []
    position = 0
    line = 1
    column = 1
    current_tag = None

    while position < len(characters):
        for pattern, tag in patterns:
            match = pattern.match(characters, position)
            if match:
                current_tag = tag
                break
        assert match is not None
        value = match.group(0)

        if current_tag == "error":
            raise Exception(f"Unexpected character: {value!r}")

        if current_tag != "whitespace":
            token = {"tag": current_tag, "line": line, "column": column}
            if current_tag == "number":
                if "." in value:
                    token["value"] = float(value)
                else:
                    token["value"] = int(value)
            tokens.append(token)

        # advance position and update line/column
        for ch in value:
            if ch == "\n":
                line += 1
                column = 1
            else:
                column += 1
        position = match.end()

    tokens.append({"tag": None, "line": line, "column": column})
    return tokens
