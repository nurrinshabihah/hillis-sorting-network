# evaluation.py
# Binary test generation, correctness checking, and fitness evaluation.
# Fitness is based on the zero-one principle: a network correct on all binary
# inputs is correct on all inputs of the same length.

from itertools import product
from typing import List
from network import Network, run_network, is_sorted


def all_binary_inputs(n_wires: int) -> List[List[int]]:
    """
    Generate all 2^n binary input sequences of length n_wires.
    Used to exhaustively verify correctness via the zero-one principle.
    """
    return [list(bits) for bits in product([0, 1], repeat=n_wires)]


def count_sorted_cases(network: Network, test_cases: List[List[int]]) -> int:
    """
    Count the number of test cases that the network sorts correctly.
    """
    score = 0
    for case in test_cases:
        output = run_network(network, case)
        if is_sorted(output):
            score += 1
    return score


def correctness_ratio(network: Network, n_wires: int) -> float:
    """
    Return the proportion of all binary inputs that the network sorts correctly.
    A ratio of 1.0 indicates a fully correct sorting network.
    """
    tests = all_binary_inputs(n_wires)
    return count_sorted_cases(network, tests) / len(tests)


def network_fitness(network: Network, n_wires: int, length_penalty: float = 0.01) -> float:
    """
    Compute the fitness of a sorting network.

    Fitness = correctness_ratio - length_penalty * len(network)

    The length penalty (lambda = 0.01) is kept small to avoid penalising
    correctness, but sufficient to prefer shorter networks when correctness
    is equal across candidates.
    """
    acc = correctness_ratio(network, n_wires)
    return acc - length_penalty * len(network)
