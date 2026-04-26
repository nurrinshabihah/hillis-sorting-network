# binary test generation, correctness, fitness
from itertools import product
from typing import List, Tuple
from network import Network, run_network, is_sorted

def all_binary_inputs(n_wires: int) -> List[List[int]]:
    return [list(bits) for bits in product([0, 1], repeat=n_wires)]

def count_sorted_cases(network: Network, test_cases: List[List[int]]) -> int:
    score = 0
    for case in test_cases:
        output = run_network(network, case)
        if is_sorted(output):
            score += 1
    return score

def correctness_ratio(network: Network, n_wires: int) -> float:
    tests = all_binary_inputs(n_wires)
    return count_sorted_cases(network, tests) / len(tests)

def network_fitness(network: Network, n_wires: int, length_penalty: float = 0.01) -> float:
    """
    Higher is better.
    Main reward: sorting correctness.
    Small penalty: shorter networks are preferred.
    """
    acc = correctness_ratio(network, n_wires)
    return acc - length_penalty * len(network)
