from testfixtures import compare

from day07.day07 import calculate_total_movements, simple_cost_function, complex_cost_function

test_input = 16, 1, 2, 0, 4, 2, 7, 1, 2, 14


def test_calculate_total_movements():
    actual = calculate_total_movements(test_input, cost_function=simple_cost_function)
    compare(actual, expected=37)


def test_calculate_total_movements_complex_cost_function():
    actual = calculate_total_movements(test_input, cost_function=complex_cost_function)
    compare(actual, expected=168)
