# Evolutionary and Co-evolutionary Search for Small Sorting Networks

This project implements baseline evolutionary and Hillis-inspired co-evolutionary algorithms for evolving small sorting networks. The aim is to investigate whether co-evolving difficult test cases can improve the search for correct sorting networks compared with a standard evolutionary approach.

## Project Overview

A sorting network is a fixed sequence of compare-and-swap operations used to sort inputs of a fixed size. In this project, candidate sorting networks are evolved automatically using an evolutionary algorithm.

Two approaches are implemented:

1. **Baseline evolution**  
   A population of sorting networks is evolved using selection, crossover, and mutation.

2. **Coevolution**  
   Sorting networks are evolved together with a second population of adversarial test cases ("parasites"). Hosts are rewarded for sorting correctly, while parasites are rewarded for exposing host failures.

The project is based on the idea introduced by Hillis (1990), adapted here to small fixed-size sorting problems.

## Objectives

- Implement a sorting network simulator
- Evaluate correctness using binary test inputs
- Implement a baseline evolutionary algorithm
- Implement a co-evolutionary extension with parasite test cases
- Compare both approaches on small input sizes such as 6 and 8 wires

## Files

- `network.py` – sorting network representation and execution
- `evaluation.py` – correctness checking, binary input generation, and fitness evaluation
- `evolution.py` – baseline evolutionary algorithm
- `coevolution.py` – parasite population and co-evolutionary algorithm
- `main.py` – entry point for running experiments

## How It Works

A sorting network is represented as a list of comparator pairs such as:

```python
[(0, 1), (2, 3), (1, 3)]