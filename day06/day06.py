initial_population = 2, 1, 1, 1, 1, 1, 1, 5, 1, 1, 1, 1, 5, 1, 1, 3, 5, 1, 1, 3, 1, 1, 3, 1, 4, 4, 4, 5, 1, 1, 1, 3, 1, 3, 1, 1, 2, 2, 1, 1, 1, 5, 1, 1, 1, 5, 2, 5, 1, 1, 2, 1, 3, 3, 5, 1, 1, 4, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 1, 5, 1, 2, 1, 1, 1, 1, 5, 1, 1, 1, 1, 1, 5, 1, 1, 1, 4, 5, 1, 1, 3, 4, 1, 1, 1, 3, 5, 1, 1, 1, 2, 1, 1, 4, 1, 4, 1, 2, 1, 1, 2, 1, 5, 1, 1, 1, 5, 1, 2, 2, 1, 1, 1, 5, 1, 2, 3, 1, 1, 1, 5, 3, 2, 1, 1, 3, 1, 1, 3, 1, 3, 1, 1, 1, 5, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 3, 1, 1, 4, 1, 1, 3, 2, 1, 2, 1, 1, 2, 2, 1, 2, 1, 1, 1, 4, 1, 2, 4, 1, 1, 4, 4, 1, 1, 1, 1, 1, 4, 1, 1, 1, 2, 1, 1, 2, 1, 5, 1, 1, 1, 1, 1, 5, 1, 3, 1, 1, 2, 3, 4, 4, 1, 1, 1, 3, 2, 4, 4, 1, 1, 3, 5, 1, 1, 1, 1, 4, 1, 1, 1, 1, 1, 5, 3, 1, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 1, 1, 1, 1, 1, 1, 1, 1, 5, 1, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 3, 1, 4, 1, 1, 2, 2, 2, 1, 1, 2, 1, 1


def iterate_population_survey(initial_population, iterations):
    """ Iterates 'initial_population' by 'iterations' where each entry in 'initial_population' represents a timer """
    population = [timer for timer in initial_population]
    for iteration in range(iterations):
        new_members = 0
        iterated_population = []
        for timer in population:
            timer -= 1
            if timer < 0:
                new_members += 1
                timer = 6
            iterated_population.append(timer)
        population = iterated_population + [8] * new_members
    return population


def iterate_frequency(frequency, iterations):
    """ Iterates 'frequency' by 'iterations' where 'frequency' is a list of counts of timers """
    for iteration in range(iterations):
        new_population = [0] * 9
        for timer, number in enumerate(frequency):
            timer -= 1
            if timer < 0:
                new_population[8] = number
                new_population[6] = number
            else:
                new_population[timer] += number
        frequency = new_population
    return frequency


def get_population_count_with_each_timer(population):
    """ Convert a list of timers into a list counting the number of times each timer occurs"""
    timer_frequency = [0] * 9
    for i in population:
        timer_frequency[i] += 1
    return timer_frequency


if __name__ == "__main__":
    population = len(iterate_population_survey(initial_population, 80))
    print("After {} iterations there are {} lanternfish".format(80, population))

    timer_frequency = get_population_count_with_each_timer(initial_population)
    population = sum(iterate_frequency(timer_frequency, 256))
    print("After {} iterations there are {} lanternfish".format(256, population))
