# sorting network representation + simulator
from typing import List, Tuple
import random

Comparator = Tuple[int, int]
Network = List[Comparator]

def apply_comparator(arr: List[int], comp: Comparator) -> None:
    i, j = comp
    if i > j:
        i, j = j, i
    if arr[i] > arr[j]:
        arr[i], arr[j] = arr[j], arr[i]

def run_network(network: Network, values: List[int]) -> List[int]:
    arr = values.copy()
    for comp in network:
        apply_comparator(arr, comp)
    return arr

def is_sorted(values: List[int]) -> bool:
    return all(values[i] <= values[i + 1] for i in range(len(values) - 1))

def random_comparator(n_wires: int) -> Comparator:
    i, j = random.sample(range(n_wires), 2)
    return (min(i, j), max(i, j))

def random_network(n_wires: int, length: int) -> Network:
    return [random_comparator(n_wires) for _ in range(length)]