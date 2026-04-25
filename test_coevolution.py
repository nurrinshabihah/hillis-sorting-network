from coevolution import (
    random_parasite,
    host_fitness,
    parasite_fitness,
    mutate_parasite,
)
from network import run_network

# A very simple example host network
# This is NOT guaranteed to be perfect, just something to test with
host1 = [(0, 1), (2, 3), (0, 2), (1, 3), (1, 2)]

# Another weak host for comparison
host2 = [(0, 1), (1, 2)]

def main():
    n_wires = 4

    print("=== Test 1: random_parasite ===")
    parasite = random_parasite(n_wires, parasite_size=5)
    print("Parasite:", parasite)
    print("Number of test cases:", len(parasite))
    print("Each case length:", [len(case) for case in parasite])

    print("\n=== Test 2: host_fitness ===")
    parasite_set = [
        [1, 0, 1, 0],
        [1, 1, 0, 0],
        [0, 1, 0, 1],
        [1, 0, 0, 1],
    ]
    h1_score = host_fitness(host1, [parasite_set])
    h2_score = host_fitness(host2, [parasite_set])
    print("Host 1 fitness:", h1_score)
    print("Host 2 fitness:", h2_score)

    print("\n=== Test 3: parasite_fitness ===")
    p_score_against_h1 = parasite_fitness(parasite_set, [host1])
    p_score_against_h2 = parasite_fitness(parasite_set, [host2])
    print("Parasite fitness against host1:", p_score_against_h1)
    print("Parasite fitness against host2:", p_score_against_h2)

    print("\n=== Test 4: mutate_parasite ===")
    original = [
        [1, 0, 1, 0],
        [0, 0, 1, 1],
        [1, 1, 0, 0],
    ]
    mutated = mutate_parasite(original, mutation_rate=0.5)
    print("Original:", original)
    print("Mutated :", mutated)

if __name__ == "__main__":
    main()