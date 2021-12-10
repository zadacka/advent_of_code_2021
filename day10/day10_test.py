from testfixtures import compare, ShouldRaise

from day10.day10 import load_day10_data, check_line, calculate_syntax_score, score_completion, \
    calculate_autocomplete_score, AdventSyntaxError

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


def test__check_line__raises_syntax_error():
    with ShouldRaise(AdventSyntaxError("}")):
        check_line("{([(<{}[<>[]}>{[]{[(<()>")
    with ShouldRaise(AdventSyntaxError(")")):
        check_line("[[<[([]))<([[{}[[()]]]")
    with ShouldRaise(AdventSyntaxError("]")):
        check_line("[{[{({}]{}}([{[{{{}}([]")
    with ShouldRaise(AdventSyntaxError(")")):
        check_line("[<(<(<(<{}))><([]([]()")
    with ShouldRaise(AdventSyntaxError(">")):
        check_line("<{([([[(<>()){}]>(<<{{")


def test_syntax_score_data():
    compare(calculate_syntax_score(test_data), expected=26397)


def test_find_syntax_error_or_completion__getting_completion():
    compare(check_line("[({(<(())[]>[[{[]{<()<>>"), expected=[c for c in "}}]])})]"])
    compare(check_line("[(()[<>])]({[<{<<[]>>("), expected=[c for c in ")}>]})"])
    compare(check_line("(((({<>}<{<{<>}{[]{[]{}"), expected=[c for c in "}}>}>))))"])
    compare(check_line("{<[[]]>}<{[{[{[]{()[[[]"), expected=[c for c in "]]}}]}]}>"])
    compare(check_line("<{([{{}}[<[[[<>{}]]]>[]]"), expected=[c for c in "])}>"])


def test_score_completion():
    compare(score_completion("}}]])})]"), expected=288957)
    compare(score_completion(")}>]})"), expected=5566)
    compare(score_completion("}}>}>))))"), expected=1480781)
    compare(score_completion("]]}}]}]}>"), expected=995444)
    compare(score_completion("])}>"), expected=294)


def test_autocomplete_score_data():
    compare(calculate_autocomplete_score(test_data), expected=288957)
