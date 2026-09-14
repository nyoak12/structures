import re
from pprint import pprint


# the + means one or more tokens open for whitespace
# \d means any zero or more digits
# \ means followed by
#

#RULES
# =====
# r"...." means a raw string 
# \ back slash -> python ignores , regex picks up
# \s -> any whitespace char (space tab newline)
# \d -> any digit 0-9
# + -> one or more of the thing before it
# * -> zero or more of the thing before it
# ? -> zero or one of the thing before it
# \. -> a literal 
# . -> any single character except newline
# | -> alternation
# \+ \* \( \) -> escaped metacharacters
# general rules -> list order matters thats why error is last -> alternation is first matched left to right
#
patterns = [
    (r"\s+", "whitespace"),
    (r"\d*\.\d+|\d+\.\d*|\d+", "number"), #float version one or float version 2 or int
    (r"\+", "+"),
    (r"\-", "-"),
    (r"\/", "/"),
    (r"\%", "%"),
    (r"\*", "*"),
    (r"\(", "("),
    (r"\)", ")"),
    (r".", "error"),
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
