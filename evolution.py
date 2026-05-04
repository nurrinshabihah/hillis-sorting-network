# baseline evolution algorithm
import random
from typing import Dict, List, Tuple, Union
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
    generations: int = 200,
    verbose: bool = True,
    return_stats: bool = False
) -> Union[Network, Tuple[Network, Dict[str, Union[bool, int, float, None]]]]:
    population = [random_network(n_wires, initial_length) for _ in range(population_size)]

    best = None
    best_fit = float("-inf")
    best_correctness = 0.0
    best_length = float("inf")
    success_generation = None

    for gen in range(generations):
        fitnesses = [network_fitness(ind, n_wires) for ind in population]

        gen_best_idx = max(range(population_size), key=lambda i: fitnesses[i])
        gen_best = population[gen_best_idx]
        gen_best_fit = fitnesses[gen_best_idx]

        # Track best-ever network by:
        # 1) higher correctness
        # 2) shorter length
        # 3) higher fitness as tie-breaker
        for idx, net in enumerate(population):
            net_correctness = correctness_ratio(net, n_wires)
            net_length = len(net)
            net_fit = fitnesses[idx]

            if success_generation is None and net_correctness == 1.0:
                success_generation = gen

            better = False
            if best is None:
                better = True
            elif net_correctness > best_correctness:
                better = True
            elif net_correctness == best_correctness and net_length < best_length:
                better = True
            elif (
                net_correctness == best_correctness
                and net_length == best_length
                and net_fit > best_fit
            ):
                better = True

            if better:
                best = net.copy()
                best_correctness = net_correctness
                best_length = net_length
                best_fit = net_fit

        gen_best_acc = correctness_ratio(gen_best, n_wires)

        if verbose:
            print(
                f"Gen {gen:03d} | "
                f"best fitness={gen_best_fit:.4f} | "
                f"gen-best correctness={gen_best_acc:.4f} | "
                f"best-so-far correctness={best_correctness:.4f} | "
                f"best-so-far length={best_length}"
            )

        # evolve next generation
        new_population = [gen_best.copy()]  # elitism

        while len(new_population) < population_size:
            p1 = tournament_selection(population, fitnesses)
            p2 = tournament_selection(population, fitnesses)
            child = crossover(p1, p2)
            child = mutate(child, n_wires)
            new_population.append(child)

        population = new_population

    final_correctness = best_correctness if best is not None else 0.0
    success = final_correctness == 1.0
    ever_found_perfect = success_generation is not None

    if return_stats:
        return best, {
            "success": success,
            "ever_found_perfect": ever_found_perfect,
            "success_generation": success_generation,
            "best_fitness": best_fit,
            "final_correctness": final_correctness,
            "best_length": int(best_length) if best is not None else 0,
            "generations_ran": generations,
        }

    return best
