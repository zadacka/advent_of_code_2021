from testfixtures import compare

from day14.day14 import load_instructions, polymerize, score_polymer

test_template = "NNCB"
test_pair_insertion_rules = {
    "CH": "B",
    "HH": "N",
    "CB": "H",
    "NH": "C",
    "HB": "C",
    "HC": "B",
    "HN": "C",
    "NN": "C",
    "BH": "H",
    "NC": "B",
    "NB": "B",
    "BN": "B",
    "BB": "N",
    "BC": "B",
    "CC": "N",
    "CN": "C",
}


def test_load_instructions():
    expected = test_template, test_pair_insertion_rules
    compare(load_instructions("day14_test_data.txt"), expected=expected)


def test_polymerize():
    template = "NNCB"
    expected_results = (
        "NCNBCHB",
        "NBCCNBBBCBHCB",
        "NBBBCNCCNBBNBNBBCHBHHBCHB",
        "NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB"
    )
    for expected in expected_results:
        template = polymerize(template, test_pair_insertion_rules)
        compare(template, expected=expected)


def test_score_polymer():
    compare(score_polymer("NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB"), expected=18)


def test_integration():
    template, map = load_instructions("day14_test_data.txt")
    for _ in range(10):
        template = polymerize(template, map)
    compare(len(template), expected=3073)
    compare(score_polymer(template), expected=1588)



# def test_polymerize_industrial():
#     actual = polymerize_industrial(test_template, test_pair_insertion_rules, 40)
#     compare(actual, expected=[])