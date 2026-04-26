# main.py
import sys

from evolution import evolve_sorting_network
from coevolution import coevolve
from compare_experiments import main as run_comparison_cli
from evaluation import correctness_ratio
from network import run_network

def run_baseline():
    n_wires = 6
    best = evolve_sorting_network(
        n_wires=n_wires,
        population_size=80,
        initial_length=14,
        generations=200
    )

    print("\n[Baseline] Best network:")
    print(best)
    print("Correctness ratio:", correctness_ratio(best, n_wires))

    sample = [1, 0, 1, 0, 1, 0]
    print("Sample input: ", sample)
    print("Sample output:", run_network(best, sample))

def run_coevolution():
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

def run_compare():
    print("\n[Comparison] Running default 80-run benchmark (CSV only).")
    print("Configuration: n_wires=6,8 | trials=20 each method | output=compare_results_fixed.csv")

    original_argv = sys.argv[:]
    try:
        sys.argv = [
            "compare_experiments.py",
            "--n-wires-list",
            "6,8",
            "--trials",
            "20",
            "--csv",
            "compare_results_fixed.csv",
            "--summary-csv",
            "compare_summary_fixed.csv",
            "--summary-md",
            "compare_summary_fixed.md",
        ]
        run_comparison_cli()
    finally:
        sys.argv = original_argv

if __name__ == "__main__":
    mode = input("Enter mode (baseline / coevolution / compare): ").strip().lower()

    if mode == "baseline":
        run_baseline()
    elif mode == "coevolution":
        run_coevolution()
    elif mode == "compare":
        run_compare()
    else:
        print("Unknown mode")
