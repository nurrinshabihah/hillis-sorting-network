# baseline evolution algorithm
import random
from typing import List
from network import Network, random_network, random_comparator
from evaluation import network_fitness, correctness_ratio

def tournament_selection(population: List[Network], fitnesses: List[float], k: int = 3) -> Network:
    indices = random.sample(range(len(population)), k)
    best_idx = max(indices, key=lambda idx: fitnesses[idx])
    return population[best_idx]

def crossover(parent1: Network, parent2: Network) -> Network:
    if not parent1 or not parent2:
        return parent1.copy() if parent1 else parent2.copy()
    cut1 = random.randint(0, len(parent1))
    cut2 = random.randint(0, len(parent2))
    child = parent1[:cut1] + parent2[cut2:]
    return child

def mutate(network: Network, n_wires: int, mutation_rate: float = 0.2) -> Network:
    child = network.copy()

    # change existing comparators
    for i in range(len(child)):
        if random.random() < mutation_rate:
            child[i] = random_comparator(n_wires)

    # occasionally add comparator
    if random.random() < 0.1:
        child.append(random_comparator(n_wires))

    # occasionally remove comparator
    if len(child) > 1 and random.random() < 0.1:
        del child[random.randrange(len(child))]

    return child

def evolve_sorting_network(
    n_wires: int = 6,
    population_size: int = 100,
    initial_length: int = 12,
    generations: int = 200
):
    population = [random_network(n_wires, initial_length) for _ in range(population_size)]

    best = None
    best_fit = float("-inf")

    for gen in range(generations):
        fitnesses = [network_fitness(ind, n_wires) for ind in population]

        gen_best_idx = max(range(population_size), key=lambda i: fitnesses[i])
        gen_best = population[gen_best_idx]
        gen_best_fit = fitnesses[gen_best_idx]

        if gen_best_fit > best_fit:
            best = gen_best.copy()
            best_fit = gen_best_fit

        acc = correctness_ratio(gen_best, n_wires)
        print(f"Gen {gen:03d} | best fitness={gen_best_fit:.4f} | correctness={acc:.4f} | length={len(gen_best)}")

        if acc == 1.0:
            print("Found valid sorting network.")
            return gen_best

        new_population = [gen_best.copy()]  # elitism

        while len(new_population) < population_size:
            p1 = tournament_selection(population, fitnesses)
            p2 = tournament_selection(population, fitnesses)
            child = crossover(p1, p2)
            child = mutate(child, n_wires)
            new_population.append(child)

        population = new_population

    return best