# coevolution.py
# Hillis-inspired competitive co-evolutionary algorithm.
# Two populations evolve together: hosts (sorting networks) and parasites
# (collections of adversarial binary test cases).

import random
from typing import List
from network import Network, run_network, is_sorted, random_network
from evolution import crossover, mutate, tournament_selection

TestCase = List[int]
Parasite = List[TestCase]


def random_test_case(n_wires: int) -> TestCase:
    """Generate a single random binary test case of length n_wires."""
    return [random.randint(0, 1) for _ in range(n_wires)]


def random_parasite(n_wires: int, parasite_size: int = 10) -> Parasite:
    """
    Generate a random parasite as a collection of binary test cases.
    parasite_size=10 balances diversity of adversarial inputs against
    the cost of evaluating each host against multiple cases.
    """
    return [random_test_case(n_wires) for _ in range(parasite_size)]


def host_fitness(host: Network, parasites: List[Parasite]) -> float:
    """
    Compute host fitness as the proportion of parasite test cases sorted correctly.
    A host that sorts all adversarial cases correctly receives a fitness of 1.0.
    """
    total = 0
    count = 0

    for parasite in parasites:
        for case in parasite:
            output = run_network(host, case)
            if is_sorted(output):
                total += 1
            count += 1

    return total / count if count > 0 else 0.0


def parasite_fitness(parasite: Parasite, hosts: List[Network]) -> float:
    """
    Compute parasite fitness as the proportion of host evaluations resulting
    in incorrect sorting. A parasite that defeats all sampled hosts receives
    a fitness of 1.0.
    """
    total_failures = 0
    count = 0

    for host in hosts:
        for case in parasite:
            output = run_network(host, case)
            if not is_sorted(output):
                total_failures += 1
            count += 1

    return total_failures / count if count > 0 else 0.0


def mutate_parasite(parasite: Parasite, mutation_rate: float = 0.1) -> Parasite:
    """
    Apply bit-flip mutation to a parasite.
    Each bit in each test case is flipped independently with probability
    mutation_rate=0.1, allowing gradual exploration of adversarial inputs
    without destroying all structure inherited from the parent.
    """
    child = [case.copy() for case in parasite]

    for case in child:
        for i in range(len(case)):
            if random.random() < mutation_rate:
                case[i] = 1 - case[i]

    return child


def crossover_parasite(p1: Parasite, p2: Parasite) -> Parasite:
    """
    Apply crossover to two parasites by combining subsets of their test cases.
    Cut points are sampled independently in each parent, producing offspring
    of variable size.
    """
    if not p1 or not p2:
        return p1.copy() if p1 else p2.copy()

    cut1 = random.randint(0, len(p1))
    cut2 = random.randint(0, len(p2))
    return p1[:cut1] + p2[cut2:]


def coevolve(
    n_wires: int = 4,
    host_population_size: int = 60,
    parasite_population_size: int = 40,
    initial_network_length: int = 14,
    parasite_size: int = 10,
    generations: int = 20
) -> Network:
    """
    Run the co-evolutionary algorithm for the given number of generations.

    Each host is evaluated against 5 randomly sampled parasites per generation
    rather than the full parasite population. This reduces evaluation cost
    while maintaining competitive pressure, since parasites are themselves
    evolving toward harder test cases. The same sampling strategy applies
    to parasite evaluation against hosts.

    Elitism is applied independently to both populations.
    The best host found across all generations is returned.
    """
    host_population = [
        random_network(n_wires, initial_network_length)
        for _ in range(host_population_size)
    ]

    parasite_population = [
        random_parasite(n_wires, parasite_size)
        for _ in range(parasite_population_size)
    ]

    best_host = None
    best_host_score = float("-inf")

    for gen in range(generations):
        # evaluate each host against 5 sampled parasites
        host_fitnesses = []
        for host in host_population:
            sampled_parasites = random.sample(
                parasite_population,
                min(5, len(parasite_population))
            )
            score = host_fitness(host, sampled_parasites)
            score -= 0.01 * len(host)  # small length penalty
            host_fitnesses.append(score)

        # evaluate each parasite against 5 sampled hosts
        parasite_fitnesses = []
        for parasite in parasite_population:
            sampled_hosts = random.sample(
                host_population,
                min(5, len(host_population))
            )
            score = parasite_fitness(parasite, sampled_hosts)
            parasite_fitnesses.append(score)

        # track best host across all generations
        best_idx = max(range(len(host_population)), key=lambda i: host_fitnesses[i])
        gen_best_host = host_population[best_idx]
        gen_best_score = host_fitnesses[best_idx]

        if gen_best_score > best_host_score:
            best_host = gen_best_host.copy()
            best_host_score = gen_best_score

        print(
            f"Gen {gen:03d} | "
            f"best host fitness={gen_best_score:.4f} | "
            f"length={len(gen_best_host)} | "
            f"best parasite fitness={max(parasite_fitnesses):.4f}"
        )

        # evolve hosts with elitism
        new_hosts = [gen_best_host.copy()]
        while len(new_hosts) < host_population_size:
            p1 = tournament_selection(host_population, host_fitnesses)
            p2 = tournament_selection(host_population, host_fitnesses)
            child = crossover(p1, p2)
            child = mutate(child, n_wires)
            new_hosts.append(child)

        # evolve parasites with elitism
        best_parasite_idx = max(range(len(parasite_population)), key=lambda i: parasite_fitnesses[i])
        best_parasite = parasite_population[best_parasite_idx]

        new_parasites = [[case.copy() for case in best_parasite]]
        while len(new_parasites) < parasite_population_size:
            p1 = tournament_selection(parasite_population, parasite_fitnesses)
            p2 = tournament_selection(parasite_population, parasite_fitnesses)
            child = crossover_parasite(p1, p2)
            child = mutate_parasite(child)
            new_parasites.append(child)

        host_population = new_hosts
        parasite_population = new_parasites

    return best_host