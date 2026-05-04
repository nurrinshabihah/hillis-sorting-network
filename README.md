# Evolutionary and Co-evolutionary Search for Small Sorting Networks

This project implements baseline evolutionary and Hillis-inspired co-evolutionary algorithms for evolving small sorting networks. The aim is to investigate whether co-evolving difficult test cases can improve the search for correct sorting networks compared with a standard evolutionary approach.

## Project Overview

A sorting network is a fixed sequence of compare-and-swap operations used to sort inputs of a fixed size. In this project, candidate sorting networks are evolved automatically using an evolutionary algorithm.

Two approaches are implemented:

1. **Baseline evolution**
   A population of sorting networks is evolved using tournament selection, one-point crossover, and three-form mutation (replacement, insertion, deletion).

2. **Coevolution**
   Sorting networks (hosts) are evolved together with a second population of adversarial test cases (parasites). Hosts are rewarded for sorting correctly, while parasites are rewarded for exposing host failures. This is based on the approach introduced by Hillis (1990).

## Requirements

- Python 3.8 or later
- No external dependencies — the standard library only

## Files

| File | Description |
|---|---|
| `network.py` | Sorting network representation, comparator simulation, and random generation |
| `evaluation.py` | Binary input generation, correctness checking, and fitness computation |
| `evolution.py` | Baseline evolutionary algorithm |
| `coevolution.py` | Parasite population management and co-evolutionary algorithm |
| `main.py` | Entry point with command-line argument handling |
| `utils.py` | Shared utilities: seeding, mean, median, standard deviation |
| `test_coevolution.py` | Unit tests for core co-evolutionary functions |

## How It Works

A sorting network is represented as a list of comparator pairs. Each comparator `(i, j)` compares the values at positions `i` and `j` and swaps them if they are out of order:

```python
[(0, 1), (2, 3), (1, 3)]
```

Correctness is evaluated using the zero-one principle: a network that correctly sorts all binary inputs of length `n` is guaranteed to correctly sort all inputs of length `n`. This allows exhaustive validation using only `2^n` test cases.

## Running the Code

Run the baseline evolutionary algorithm on 6 wires with seed 42:

```bash
python main.py --mode baseline --wires 6 --seed 42
```

Run the co-evolutionary algorithm on 8 wires with seed 7:

```bash
python main.py --mode coevolution --wires 8 --seed 7
```

## Running Tests

```bash
python test_coevolution.py
```

This runs unit tests for random parasite generation, host fitness, parasite fitness, and mutation.

## Reference

Hillis, W.D. (1990). Co-evolving parasites improve simulated evolution as an optimization procedure. *Physica D: Nonlinear Phenomena*, 42(1-3), pp. 228-234.