from testfixtures import compare

from day10.day10 import load_day10_data, find_syntax_error_or_completion, syntax_score_data, score_completion, \
    autocomplete_score_data

test_data = """\
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""


def test_load_data():
    compare(load_day10_data("day10_test_data.txt"), expected=test_data)


def test_find_syntax_error():
    compare(find_syntax_error_or_completion("{([(<{}[<>[]}>{[]{[(<()>")[0], expected="}")
    compare(find_syntax_error_or_completion("[[<[([]))<([[{}[[()]]]")[0], expected=")")
    compare(find_syntax_error_or_completion("[{[{({}]{}}([{[{{{}}([]")[0], expected="]")
    compare(find_syntax_error_or_completion("[<(<(<(<{}))><([]([]()")[0], expected=")")
    compare(find_syntax_error_or_completion("<{([([[(<>()){}]>(<<{{")[0], expected=">")


def test_syntax_score_data():
    compare(syntax_score_data(test_data), expected=26397)


def test_find_syntax_error_or_completion__getting_completion():
    compare(find_syntax_error_or_completion("[({(<(())[]>[[{[]{<()<>>")[1], expected=[c for c in "}}]])})]"])
    compare(find_syntax_error_or_completion("[(()[<>])]({[<{<<[]>>(")[1], expected=[c for c in ")}>]})"])
    compare(find_syntax_error_or_completion("(((({<>}<{<{<>}{[]{[]{}")[1], expected=[c for c in "}}>}>))))"])
    compare(find_syntax_error_or_completion("{<[[]]>}<{[{[{[]{()[[[]")[1], expected=[c for c in "]]}}]}]}>"])
    compare(find_syntax_error_or_completion("<{([{{}}[<[[[<>{}]]]>[]]")[1], expected=[c for c in "])}>"])


def test_score_completion():
    compare(score_completion("}}]])})]"), expected=288957)
    compare(score_completion(")}>]})"), expected=5566)
    compare(score_completion("}}>}>))))"), expected=1480781)
    compare(score_completion("]]}}]}]}>"), expected=995444)
    compare(score_completion("])}>"), expected=294)


def test_autocomplete_score_data():
    compare(autocomplete_score_data(test_data), expected=288957)
