from testfixtures import compare

from day06.day06 import iterate_population_survey, iterate_frequency, get_population_count_with_each_timer

test_input = 3, 4, 3, 1, 2


def test_iterate_population():
    actual = iterate_population_survey(test_input, iterations=1)
    compare(actual, expected=[2, 3, 2, 0, 1])

    actual18 = iterate_population_survey(test_input, iterations=18)
    compare(actual18, expected=[6, 0, 6, 4, 5, 6, 0, 1, 1, 2, 6, 0, 1, 1, 1, 2, 2, 3, 3, 4, 6, 7, 8, 8, 8, 8])


def test_get_population_timer_frequency():
    compare([3, 5, 3, 2, 2, 1, 5, 1, 4], actual=get_population_count_with_each_timer(
        [6, 0, 6, 4, 5, 6, 0, 1, 1, 2, 6, 0, 1, 1, 1, 2, 2, 3, 3, 4, 6, 7, 8, 8, 8, 8]))


def test_iterate_count_population():
    population = get_population_count_with_each_timer(test_input)
    population = iterate_frequency(population, 1)
    compare(population, expected=get_population_count_with_each_timer([2, 3, 2, 0, 1]))
    population = iterate_frequency(population, 1)
    compare(population, expected=get_population_count_with_each_timer([1, 2, 1, 6, 0, 8]))



def test_population_growth():
    timer_frequency = get_population_count_with_each_timer(test_input)
    population = sum(iterate_frequency(timer_frequency, 256))
    compare(population, expected=26984457539)
