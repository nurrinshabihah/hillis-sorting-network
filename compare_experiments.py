import argparse
import csv
import random
import statistics
import time
from typing import Any, Dict, List

from coevolution import coevolve
from evolution import evolve_sorting_network

# ---------------------------------------------------------------------------
# Statistics helpers
# ---------------------------------------------------------------------------


def summarize(values: List[float]) -> Dict[str, float]:
    """Return mean/median/population-stdev for a numeric list."""
    if not values:
        return {"mean": 0.0, "median": 0.0, "stdev": 0.0}
    return {
        "mean": statistics.mean(values),
        "median": statistics.median(values),
        "stdev": statistics.pstdev(values),
    }


def run_baseline_trial(seed: int, args: argparse.Namespace) -> Dict[str, Any]:
    """Run one baseline-evolution trial for the provided seed."""
    random.seed(seed)
    _, stats = evolve_sorting_network(
        n_wires=args.n_wires,
        population_size=args.baseline_population,
        initial_length=args.initial_length,
        generations=args.baseline_generations,
        verbose=False,
        return_stats=True,
    )
    return stats


def run_coevolution_trial(seed: int, args: argparse.Namespace) -> Dict[str, Any]:
    """Run one coevolution trial for the provided seed."""
    random.seed(seed)
    _, stats = coevolve(
        n_wires=args.n_wires,
        host_population_size=args.host_population,
        parasite_population_size=args.parasite_population,
        initial_network_length=args.initial_length,
        parasite_size=args.parasite_size,
        generations=args.coevolution_generations,
        verbose=False,
        return_stats=True,
    )
    return stats


def aggregate_results(rows: List[Dict[str, Any]], method_name: str) -> Dict[str, Any]:
    """Aggregate per-run rows into summary metrics for one method."""
    successes = [int(bool(r["success"])) for r in rows]
    success_rate = (sum(successes) / len(successes)) if rows else 0.0
    ever_found = [int(bool(r.get("ever_found_perfect", False))) for r in rows]
    ever_found_rate = (sum(ever_found) / len(ever_found)) if rows else 0.0

    correctness_values = [float(r["final_correctness"]) for r in rows]
    length_values = [float(r["best_length"]) for r in rows]
    runtime_values = [float(r["runtime_seconds"]) for r in rows]

    success_generations = [
        float(r["success_generation"])
        for r in rows
        if bool(r.get("ever_found_perfect", False)) and r["success_generation"] is not None
    ]

    correctness_summary = summarize(correctness_values)
    length_summary = summarize(length_values)
    runtime_summary = summarize(runtime_values)
    speed_summary = summarize(success_generations) if success_generations else None

    result: Dict[str, Any] = {
        "method": method_name,
        "trials": len(rows),
        "success_rate": success_rate,
        "ever_found_perfect_rate": ever_found_rate,
        "correctness_mean": correctness_summary["mean"],
        "correctness_median": correctness_summary["median"],
        "correctness_stdev": correctness_summary["stdev"],
        "length_mean": length_summary["mean"],
        "length_median": length_summary["median"],
        "length_stdev": length_summary["stdev"],
        "runtime_mean_seconds": runtime_summary["mean"],
        "runtime_median_seconds": runtime_summary["median"],
    }
    if speed_summary is not None:
        result["success_generation_mean"] = speed_summary["mean"]
        result["success_generation_median"] = speed_summary["median"]
    else:
        result["success_generation_mean"] = None
        result["success_generation_median"] = None
    return result


# ---------------------------------------------------------------------------
# Console output helpers
# ---------------------------------------------------------------------------

def print_method_summary(summary: Dict[str, Any]) -> None:
    """Print a human-readable summary block for one method."""
    print(f"\n=== {summary['method']} ===")
    print(f"Trials: {summary['trials']}")
    print(f"Success rate (final network perfect): {summary['success_rate']:.2%}")
    print(f"Ever found perfect during run: {summary['ever_found_perfect_rate']:.2%}")
    print(
        "Final correctness (mean / median / stdev): "
        f"{summary['correctness_mean']:.4f} / "
        f"{summary['correctness_median']:.4f} / "
        f"{summary['correctness_stdev']:.4f}"
    )
    print(
        "Best length (mean / median / stdev): "
        f"{summary['length_mean']:.2f} / "
        f"{summary['length_median']:.2f} / "
        f"{summary['length_stdev']:.2f}"
    )
    print(
        "Runtime seconds (mean / median): "
        f"{summary['runtime_mean_seconds']:.4f} / "
        f"{summary['runtime_median_seconds']:.4f}"
    )
    if summary["success_generation_mean"] is None:
        print("Convergence generation: no successful runs")
    else:
        print(
            "Generation first found perfect (mean / median, among runs that ever found one): "
            f"{summary['success_generation_mean']:.2f} / "
            f"{summary['success_generation_median']:.2f}"
        )


# ---------------------------------------------------------------------------
# File output helpers
# ---------------------------------------------------------------------------

def maybe_write_csv(path: str, rows: List[Dict[str, Any]]) -> None:
    """Write per-run detailed results CSV using the required schema."""
    if not rows:
        return

    fieldnames = [
    "method",
    "n_wires",
    "run_id",
    "found_valid",
    "generation_found",
    "final_correctness",
    "best_length",
    "time_seconds",
]

    normalized_rows: List[Dict[str, Any]] = []
    for row in rows:
        normalized_rows.append(
            {
                "method": row.get("method"),
                "n_wires": row.get("n_wires"),
                "run_id": row.get("trial"),
                "found_valid": bool(row.get("success")),
                "generation_found": row.get("success_generation"),
                "final_correctness": row.get("final_correctness"),
                "best_length": row.get("best_length"),
                "time_seconds": row.get("runtime_seconds"),
            }
        )

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(normalized_rows)
    print(f"\nWrote detailed trial results to: {path}")


def maybe_write_summary_csv(path: str, summary_rows: List[Dict[str, Any]]) -> None:
    """Write aggregated per-method summaries to CSV."""
    if not summary_rows:
        return

    fieldnames = [
        "n_wires",
        "method",
        "trials",
        "success_rate",
        "ever_found_perfect_rate",
        "correctness_mean",
        "correctness_median",
        "correctness_stdev",
        "length_mean",
        "length_median",
        "length_stdev",
        "runtime_mean_seconds",
        "runtime_median_seconds",
        "success_generation_mean",
        "success_generation_median",
    ]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summary_rows)
    print(f"Wrote summary metrics CSV to: {path}")


def maybe_write_summary_markdown(path: str, summary_rows: List[Dict[str, Any]]) -> None:
    """Write a compact markdown table for quick reading/sharing."""
    if not summary_rows:
        return

    lines: List[str] = []
    lines.append("# Comparison Summary")
    lines.append("")
    lines.append(
        "| n_wires | method | trials | success_rate | correctness (mean/median/stdev) | "
        "length (mean/median/stdev) | runtime_s (mean/median) | gen_found (mean/median) |"
    )
    lines.append(
        "|---:|---|---:|---:|---|---|---|---|"
    )

    for row in summary_rows:
        gen_text = (
            "N/A"
            if row["success_generation_mean"] is None
            else f"{row['success_generation_mean']:.2f}/{row['success_generation_median']:.2f}"
        )
        lines.append(
            f"| {row['n_wires']} | {row['method']} | {row['trials']} | "
            f"{row['success_rate']:.2%} | "
            f"{row['correctness_mean']:.4f}/{row['correctness_median']:.4f}/{row['correctness_stdev']:.4f} | "
            f"{row['length_mean']:.2f}/{row['length_median']:.2f}/{row['length_stdev']:.2f} | "
            f"{row['runtime_mean_seconds']:.4f}/{row['runtime_median_seconds']:.4f} | "
            f"{gen_text} |"
        )

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Wrote readable summary report to: {path}")


# ---------------------------------------------------------------------------
# Main experiment driver
# ---------------------------------------------------------------------------

def main() -> None:
    """Run baseline vs coevolution comparisons and export results."""
    parser = argparse.ArgumentParser(
        description="Compare baseline evolution vs coevolution over multiple seeds."
    )
    parser.add_argument("--trials", type=int, default=30, help="Number of runs per method.")
    parser.add_argument("--seed-start", type=int, default=0, help="Starting seed value.")
    parser.add_argument("--n-wires", type=int, default=6, help="Number of wires.")
    parser.add_argument(
        "--n-wires-list",
        type=str,
        default="",
        help="Optional comma-separated wire counts (e.g. 6,8). If set, runs all listed values.",
    )
    parser.add_argument("--initial-length", type=int, default=14, help="Initial network length.")
    parser.add_argument("--baseline-population", type=int, default=80)
    parser.add_argument("--baseline-generations", type=int, default=300)
    parser.add_argument("--host-population", type=int, default=60)
    parser.add_argument("--parasite-population", type=int, default=40)
    parser.add_argument("--parasite-size", type=int, default=10)
    parser.add_argument("--coevolution-generations", type=int, default=200)
    parser.add_argument(
        "--csv",
        type=str,
        default="compare_results.csv",
        help="Path to write per-trial results as CSV. Empty value disables CSV.",
    )
    parser.add_argument(
        "--summary-csv",
        type=str,
        default="compare_summary.csv",
        help="Path to write aggregated summary metrics as CSV. Empty value disables summary CSV.",
    )
    parser.add_argument(
        "--summary-md",
        type=str,
        default="compare_summary.md",
        help="Path to write a readable markdown summary table. Empty value disables summary markdown.",
    )
    args = parser.parse_args()

    # Support either a single --n-wires value or a comma-separated list.
    n_wires_values = (
        [int(v.strip()) for v in args.n_wires_list.split(",") if v.strip()]
        if args.n_wires_list.strip()
        else [args.n_wires]
    )

    all_rows: List[Dict[str, Any]] = []
    all_summaries: List[Dict[str, Any]] = []

    for n_wires in n_wires_values:
        print(f"\n##### Running experiment set for n_wires={n_wires} #####")
        args.n_wires = n_wires
        baseline_rows: List[Dict[str, Any]] = []
        coevolution_rows: List[Dict[str, Any]] = []

        # Each trial uses the same seed for baseline and coevolution.
        for i in range(args.trials):
            seed = args.seed_start + i
            print(f"Running trial {i + 1}/{args.trials} with seed={seed} ...")

            baseline_start = time.perf_counter()
            baseline_stats = run_baseline_trial(seed, args)
            baseline_runtime = time.perf_counter() - baseline_start
            baseline_rows.append(
                {
                    "n_wires": n_wires,
                    "method": "baseline",
                    "trial": i + 1,
                    "seed": seed,
                    "runtime_seconds": baseline_runtime,
                    **baseline_stats,
                }
            )

            coev_start = time.perf_counter()
            coev_stats = run_coevolution_trial(seed, args)
            coev_runtime = time.perf_counter() - coev_start
            coevolution_rows.append(
                {
                    "n_wires": n_wires,
                    "method": "coevolution",
                    "trial": i + 1,
                    "seed": seed,
                    "runtime_seconds": coev_runtime,
                    **coev_stats,
                }
            )

        # Compute and print per-method summary for this wire count.
        baseline_summary = aggregate_results(
            baseline_rows, f"Baseline Evolution (n_wires={n_wires})"
        )
        coev_summary = aggregate_results(
            coevolution_rows, f"Hillis-style Coevolution (n_wires={n_wires})"
        )
        print_method_summary(baseline_summary)
        print_method_summary(coev_summary)
        all_rows.extend(baseline_rows + coevolution_rows)
        all_summaries.extend(
            [
                {
                    **baseline_summary,
                    "n_wires": n_wires,
                    "method": "baseline",
                },
                {
                    **coev_summary,
                    "n_wires": n_wires,
                    "method": "coevolution",
                },
            ]
        )

    # Persist full outputs after all wire-count sets complete.
    csv_path = args.csv.strip()
    if csv_path:
        maybe_write_csv(csv_path, all_rows)
    summary_csv_path = args.summary_csv.strip()
    if summary_csv_path:
        maybe_write_summary_csv(summary_csv_path, all_summaries)
    summary_md_path = args.summary_md.strip()
    if summary_md_path:
        maybe_write_summary_markdown(summary_md_path, all_summaries)


if __name__ == "__main__":
    main()
