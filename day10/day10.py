import os.path
from termcolor import cprint


# def SyntaxError(Exception):
#     pass


def load_day10_data(filename):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath) as f:
        return f.read()


def find_syntax_error_or_completion(line):
    open_brackets = {"(": ")", "[": "]", "{": "}", "<": ">"}
    close_brackets = {v: k for k, v in open_brackets.items()}
    stack = []
    for character in line.strip():
        if character in open_brackets:
            stack.append(character)
        elif character in close_brackets:
            if stack and stack[-1] == close_brackets[character]:
                stack.pop()
            else:
                return character, []
        else:
            raise ValueError("Unexpected: {} found!".format(character))
    return None, [open_brackets[c] for c in stack[::-1]]


def score_syntax_error(character):
    scores = {")": 3, "]": 57, "}": 1197, ">": 25137, None: 0}
    return scores[character]


def score_completion(characters):
    total = 0
    scores = {")": 1, "]": 2, "}": 3, ">": 4}
    for c in characters:
        total = (total * 5) + scores[c]
    return total


def syntax_score_data(lines):
    syntax_errors = [find_syntax_error_or_completion(line)[0] for line in lines.split('\n')]
    scores = [score_syntax_error(e) for e in syntax_errors]
    return sum(scores)


def autocomplete_score_data(data):
    autocompletions = [find_syntax_error_or_completion(line)[1] for line in data.split('\n')]
    scores = [score_completion(c) for c in autocompletions if c]
    return sorted(scores)[len(scores) // 2]


if __name__ == "__main__":
    data = load_day10_data("day10_real_data.txt")
    print("The syntax error score is {}".format(syntax_score_data(data)))
    print("The autocomplete score is {}".format(autocomplete_score_data(data)))
