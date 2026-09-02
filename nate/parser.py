# parser.py

from tokenizer import tokenize
from pprint import pprint

# EBNF

#   expression = term { ("+" | "-") term }
#   term = factor { ("*" | "/") factor }
#   factor = <number> | "(" expression ")"


def parse_factor(tokens):
    """factor = <number> | "(" expression ")"""
    token = tokens[0]
    if token["tag"] == "number":
        node = {"tag": "number", "value": token["value"]}
        return node, tokens[1:]
    if token["tag"] == "(":
        node, tokens = parse_expression(tokens[1:])
        if tokens[0]["tag"] != ")":
            raise SyntaxError(f"Expected ')', got {tokens[0]}")
        return node, tokens[1:]
    raise SyntaxError(f"Expected expression, got {tokens[0]}")

