#!/usr/bin/python3

from statistics import mean
import sys
import textwrap
import numpy as np
import time


# Argument usage helper
def show_usage():
    help = textwrap.dedent('''
    NAME
        Python 3 Knapsack Problem Analysis
    SYNOPSIS
        contenedor.py [-h] algorithm -a file.txt iterations
        contenedor.py [-h] algorithm -p capacity N weights benefits iterations
    DESCRIPTION
    
    ALGORITHM
        Desired algorithm to solve the problem.
        1 = 
        2 = 
        3 = 
        4 =
    FILE 
        Text file with the knapsack problem in the correct format
    CAPACITY
        Max weight of the knapsack
    N
        Number of items
    WEIGHT RANGES
        Generate a random weight list between those values
    BENEFIT RANGES
        Generate a random benefit list between those values
    ITERATIONS
        Number of times the algorithm should be run
    ''')
    print(help)


# Remove program name from arguments
args = sys.argv[1:]

# Algorithm constants
BRUTE_FORCE = 1
BOTTOM_UP = 2
TOP_DOWN = 3
COMPARE_ALL = 4


def brute_force_knapsack(capacity: int, weights: list, benefits: list, n: int, elements_used: list) -> int:
    # hold the elements of the two combinations  
    case_1 = []
    case_2 = []

    # Base Case
    if n == 0 or capacity <= 0:
        return 0

    # each item's weight can't be more than capacity
    if weights[n - 1] > capacity:
        return brute_force_knapsack(capacity, weights, benefits, n - 1, case_2)

    else:
        case_1.append(n)  # put the element in case_1 and pass case_1
        combination_1 = benefits[n - 1] + brute_force_knapsack(capacity - weights[n - 1], weights, benefits, n - 1,
                                                               case_1)
        # don't put anything in case_2 but pass case_2
        combination_2 = brute_force_knapsack(capacity, weights, benefits, n - 1, case_2)
        # get the max situation between the two combinations
        max_value = max(combination_1, combination_2)
        # if this situation occurs then nth item is included

        if max_value == combination_1:
            elements_used += case_1
        else:
            elements_used += case_2

        print(f'elements used: {elements_used}')

        return max_value


def top_down_knapsack(capacity: int, weights: list, benefits: list, current: int, memo: list, elements_used: list):
    if capacity <= 0 or current == len(benefits):
        return 0, []

    if memo[current][capacity] is not None:
        return memo[current][capacity]

    included_benefit, included = -1, []
    if weights[current] <= capacity:
        included_benefit, included = top_down_knapsack(capacity - weights[current],
                                                       weights, benefits,
                                                       current + 1, memo, elements_used)
        included_benefit += benefits[current]
        included.append(current + 1)

    not_included_benefit, not_included = \
        top_down_knapsack(capacity, weights, benefits, current + 1, memo, elements_used)

    if included_benefit >= not_included_benefit:
        elements_used = included
        memo[current][capacity] = included_benefit, elements_used

    else:
        elements_used = not_included
        memo[current][capacity] = not_included_benefit, elements_used

    return memo[current][capacity]


def run_from_file():
    capacity, weights, benefits = generate_problem_from_file()
    n = len(benefits)
    algorithm = int(args[0])
    iterations = int(args[3])
    print(f'Capacity: {capacity} N: {n} Weights: {weights} Benefits: {benefits}')
    knapsack_params = (capacity, weights, benefits, n)
    choose_measure(algorithm, iterations, knapsack_params)


def generate_problem_from_file() -> tuple:
    file = open(args[2], 'r')
    capacity = int(file.readline())
    weights, benefits = [], []
    for line in file:
        w, b = map(int, line.split(","))
        weights.append(w)
        benefits.append(b)
    file.close()
    return capacity, weights, benefits


def run_from_random():
    algorithm = int(args[0])
    capacity = int(args[2])
    n = int(args[3])
    iterations = int(args[6])
    weights, benefits = generate_problem_from_random(n)
    print(f'Capacity: {capacity} N: {n} Weights: {weights} Benefits: {benefits}')
    knapsack_params = (capacity, weights, benefits, n)
    choose_measure(algorithm, iterations, knapsack_params)


def generate_problem_from_random(n: int) -> tuple:
    low_weight, high_weight = map(int, args[4].split(sep="-"))
    low_benefit, high_benefit = map(int, args[5].split(sep="-"))
    rng = np.random.default_rng()
    weights = list(rng.integers(low=low_weight, high=high_weight, size=n))
    benefits = list(rng.integers(low=low_benefit, high=high_benefit, size=n))
    return weights, benefits


def measure(algorithm, iterations: int) -> list:
    runtimes, result, items_used = [], [], []
    for _ in range(iterations):
        begin = time.time()
        result, items_used = algorithm
        end = time.time()
        runtime = end - begin
        runtimes.append(runtime)
    items_used.reverse()
    print(f'Result: {result}\nItems used: {items_used}')
    return runtimes


def measure_top_down(iterations: int, knapsack_params):
    capacity, weights, benefits, _ = knapsack_params
    memo = [[None for _ in range(capacity + 1)] for _ in range(len(benefits))]
    knapsack_params = capacity, weights, benefits, 0, memo
    measures = measure(top_down_knapsack(*knapsack_params, elements_used=[]), iterations)
    return measures


def measure_bottom_up():
    pass


def measure_brute(iterations: int, knapsack_params):
    measures = measure(brute_force_knapsack(*knapsack_params, elements_used=[]), iterations)
    return measures


def choose_measure(algorithm: int, iterations: int, knapsack_params: tuple):
    measurers = {
        TOP_DOWN: {measure_top_down},
        BOTTOM_UP: {measure_bottom_up},
        BRUTE_FORCE: {measure_brute},
        COMPARE_ALL: {measure_top_down, measure_bottom_up, measure_brute}
    }.get(algorithm)

    measurements = []
    for measurer in measurers:
        measurements.append(measurer(iterations, knapsack_params))

    if algorithm == COMPARE_ALL:
        pass


def main():
    if '-a' in args:
        run_from_file()

    elif '-p' in args:
        run_from_random()

    else:
        show_usage()


if __name__ == "__main__":
    main()
