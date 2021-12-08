from testfixtures import compare

from day08.day08 import load_data, count_uniques, get_wire_to_segment_map, translate_code_to_number, \
    calculate_remaining_digits_value, get_total

test_data = (
    (["be", "cfbegad", "cbdgef", "fgaecd", "cgeb", "fdcge", "agebfd", "fecdb", "fabcd", "edb"],
     ["fdgacbe", "cefdb", "cefbgd", "gcbe"]),
    (["edbfga", "begcd", "cbg", "gc", "gcadebf", "fbgde", "acbgfd", "abcde", "gfcbed", "gfec"],
     ["fcgedb", "cgb", "dgebacf", "gc"]),
    (["fgaebd", "cg", "bdaec", "gdafb", "agbcfd", "gdcbef", "bgcad", "gfac", "gcb", "cdgabef"],
     ["cg", "cg", "fdcagb", "cbg"]),
    (["fbegcd", "cbd", "adcefb", "dageb", "afcb", "bc", "aefdc", "ecdab", "fgdeca", "fcdbega"],
     ["efabcd", "cedba", "gadfec", "cb"]),
    (["aecbfdg", "fbg", "gf", "bafeg", "dbefa", "fcge", "gcbea", "fcaegb", "dgceab", "fcbdga"],
     ["gecf", "egdcabf", "bgf", "bfgea"]),
    (["fgeab", "ca", "afcebg", "bdacfeg", "cfaedg", "gcfdb", "baec", "bfadeg", "bafgc", "acf"],
     ["gebdcfa", "ecba", "ca", "fadegcb"]),
    (["dbcfg", "fgd", "bdegcaf", "fgec", "aegbdf", "ecdfab", "fbedc", "dacgb", "gdcebf", "gf"],
     ["cefg", "dcbef", "fcge", "gbcadfe"]),
    (["bdfegc", "cbegaf", "gecbf", "dfcage", "bdacg", "ed", "bedf", "ced", "adcbefg", "gebcd"],
     ["ed", "bcgafe", "cdgba", "cbgef"]),
    (["egadfb", "cdbfeg", "cegd", "fecab", "cgb", "gbdefca", "cg", "fgcdab", "egfdb", "bfceg"],
     ["gbdfcae", "bgc", "cg", "cgb"]),
    (["gcafb", "gcf", "dcaebfg", "ecagb", "gf", "abcdeg", "gaef", "cafbge", "fdbac", "fegbdc"],
     ["fgae", "cfgab", "fg", "bagce"]),
)


def test_get_wire_to_segment_map():
    actual = get_wire_to_segment_map(
        (["acedgfb", "cdfbe", "gcdfa", "fbcad", "dab", "cefabd", "cdfgeb", "eafb", "cagedb", "ab"]))
    expected = {'d': 'a', 'e': 'b', 'a': 'c', 'f': 'd', 'g': 'e', 'b': 'f', 'c': 'g'}
    compare(actual, expected=expected)

def test_translate_code_to_number():
    mapping = {'d': 'a', 'e': 'b', 'a': 'c', 'f': 'd', 'g': 'e', 'b': 'f', 'c': 'g'}
    actual = translate_code_to_number(mapping, "cdfeb")
    compare(actual, expected=5)

def test_calculate_remaining_digits_value():
    mapping = {'d': 'a', 'e': 'b', 'a': 'c', 'f': 'd', 'g': 'e', 'b': 'f', 'c': 'g'}
    signal_patterns = ["cdfeb", "fcadb", "cdfeb", "cdbaf",]
    actual = calculate_remaining_digits_value(mapping, signal_patterns)
    compare(actual, expected=5353)


def test_load_data():
    actual = load_data("day08_test_data.txt")
    compare(actual, expected=test_data)


def test_count_uniques():
    actual = count_uniques(test_data)
    compare(actual, expected=26)

def test_part_b_integration_test():
    data = load_data("day08_test_data.txt")
    total = get_total(data)
    compare(total, expected=61229)