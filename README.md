# Evolutionary and Co-evolutionary Search for Small Sorting Networks

This project implements a baseline evolutionary algorithm and a Hillis-style co-evolutionary algorithm for evolving small sorting networks.

The goal is to compare the two approaches on small fixed-size sorting problems in terms of:

* correctness
* convergence behaviour
* network size
* runtime

## Overview

A sorting network is a fixed sequence of compare-and-swap operations for sorting inputs of a fixed size.

Two approaches are implemented:

* **Baseline evolution**
  Evolves a population of sorting networks using tournament selection, crossover, and mutation.

* **Coevolution**
  Evolves sorting networks (**hosts**) together with adversarial binary test sets (**parasites**). Hosts are rewarded for sorting correctly, while parasites are rewarded for exposing failures.

## Experimental Setup

The main comparison uses:

* **Problem sizes:** `n = 6` and `n = 8` wires
* **Trials:** 20 runs per method per problem size
* **Total runs:** 80
* **Baseline:** population size 80, 200 generations
* **Coevolution:** host population 60, parasite population 40, 200 generations
* **Initial network length:** 14 comparators

Final solutions are validated exhaustively on all `2^n` binary inputs.

## Requirements

### Core code

* Python 3.8+
* standard library only

### Plotting

For plotting scripts, install:

```bash
pip install pandas matplotlib
```

## Running the Code

Run:

```bash
python main.py
```

Then choose one of:

* `baseline`
* `coevolution`
* `compare`

### Modes

* `baseline`
  Runs one baseline search on 6 wires.

* `coevolution`
  Runs one co-evolutionary search on 6 wires.

* `compare`
  Runs the full benchmark for:

  * baseline and coevolution
  * 6 and 8 wires
  * 20 trials each

## Output

### Per-run CSV

Contains one row per run, including:

* `method`
* `n_wires`
* `run_id`
* `found_valid`
* `generation_found`
* `final_correctness`
* `best_length`
* `time_seconds`

### Summary CSV

Contains aggregated results for each method and wire count.


## Plotting

```bash
python plot_results.py
```


## Notes

This is a simplified adaptation of Hillis (1990), not a direct reproduction. It keeps the host–parasite idea, but uses a simpler direct encoding and standard evolutionary operators.



## Reference

Hillis, W. D. (1990). *Co-evolving parasites improve simulated evolution as an optimization procedure*. Physica D: Nonlinear Phenomena, 42(1–3), 228–234.
