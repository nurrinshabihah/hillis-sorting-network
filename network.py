# network.py
# Sorting network representation and simulator.
# A network is a list of comparator pairs (i, j) applied sequentially to an input array.

from typing import List, Tuple
import random

Comparator = Tuple[int, int]
Network = List[Comparator]


def apply_comparator(arr: List[int], comp: Comparator) -> None:
    """
    Apply a single comparator to an array in place.
    Swaps arr[i] and arr[j] if arr[i] > arr[j], ensuring the smaller value
    moves to the lower index.
    """
    i, j = comp
    if i > j:
        i, j = j, i
    if arr[i] > arr[j]:
        arr[i], arr[j] = arr[j], arr[i]


def run_network(network: Network, values: List[int]) -> List[int]:
    """
    Apply all comparators in the network sequentially to a copy of the input.
    Returns the resulting array without modifying the original.
    """
    arr = values.copy()
    for comp in network:
        apply_comparator(arr, comp)
    return arr


def is_sorted(values: List[int]) -> bool:
    """Return True if values is non-decreasing, False otherwise."""
    return all(values[i] <= values[i + 1] for i in range(len(values) - 1))


def random_comparator(n_wires: int) -> Comparator:
    """
    Generate a random valid comparator (i, j) with i < j,
    sampled uniformly from all wire pairs.
    """
    i, j = random.sample(range(n_wires), 2)
    return (min(i, j), max(i, j))


def random_network(n_wires: int, length: int) -> Network:
    """
    Generate a random sorting network of a given length by uniformly
    sampling valid comparator pairs.
    """
    return [random_comparator(n_wires) for _ in range(length)]