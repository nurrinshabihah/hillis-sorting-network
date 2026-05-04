# main.py
from evolution import evolve_sorting_network
from coevolution import coevolve
from evaluation import correctness_ratio
from network import run_network

def run_baseline():
    """Run the baseline evolutionary algorithm and print results."""
    n_wires = 6
    best = evolve_sorting_network(
        n_wires=n_wires,
        population_size=80,
        initial_length=14,
        generations=300
    )

    print("\n[Baseline] Best network:")
    print(best)
    print("Correctness ratio:", correctness_ratio(best, n_wires))

    sample = [1, 0, 1, 0, 1, 0]
    print("Sample input: ", sample)
    print("Sample output:", run_network(best, sample))

def run_coevolution():
    """Run the co-evolutionary algorithm and print results."""
    n_wires = 6
    best = coevolve(
        n_wires=n_wires,
        host_population_size=60,
        parasite_population_size=40,
        initial_network_length=14,
        parasite_size=10,
        generations=200
    )

    print("\n[Coevolution] Best host network:")
    print(best)
    print("Correctness ratio on all binary inputs:", correctness_ratio(best, n_wires))

    sample = [1, 0, 1, 0, 1, 0]
    print("Sample input: ", sample)
    print("Sample output:", run_network(best, sample))

if __name__ == "__main__":
    mode = input("Enter mode (baseline / coevolution): ").strip().lower()

    if mode == "baseline":
        run_baseline()
    elif mode == "coevolution":
        run_coevolution()
    else:
        print("Unknown mode")