import os.path


class AdventSyntaxError(Exception):
    def __init__(self, bad_character, *args: object) -> None:
        super().__init__(*args)
        self.bad_character = bad_character


def load_day10_data(filename):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath) as f:
        return f.read()


def check_line(line):
    open_brackets = {"(": ")", "[": "]", "{": "}", "<": ">"}
    close_brackets = {v: k for k, v in open_brackets.items()}
    stack = []
    for character in line:
        if character in open_brackets:
            stack.append(character)
        elif character in close_brackets:
            if stack and stack[-1] == close_brackets[character]:
                stack.pop()
            else:
                raise AdventSyntaxError(character)
        else:
            raise ValueError("Unexpected: {} found!".format(character))
    closing_brackets_required = [open_brackets[c] for c in stack[::-1]]
    return closing_brackets_required


def score_syntax_error(character):
    scores = {")": 3, "]": 57, "}": 1197, ">": 25137}
    return scores[character]


def score_completion(characters):
    total = 0
    scores = {")": 1, "]": 2, "}": 3, ">": 4}
    for c in characters:
        total = (total * 5) + scores[c]
    return total


def calculate_syntax_score(data):
    syntax_errors, completions = process_data(data)
    scores = [score_syntax_error(e) for e in syntax_errors]
    return sum(scores)


def calculate_autocomplete_score(data):
    syntax_errors, completions = process_data(data)
    scores = [score_completion(c) for c in completions]
    return sorted(scores)[len(scores) // 2]


def process_data(data):
    syntax_errors = []
    completions = []
    for line in data.split('\n'):
        try:
            completion = check_line(line)
            completions.append(completion)
        except AdventSyntaxError as e:
            syntax_errors.append(e.bad_character)
    return syntax_errors, completions


if __name__ == "__main__":
    navigation_data = load_day10_data("day10_real_data.txt")
    print("The syntax error score is {}".format(calculate_syntax_score(navigation_data)))
    print("The autocomplete score is {}".format(calculate_autocomplete_score(navigation_data)))
