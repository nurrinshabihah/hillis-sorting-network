# coevolution.py
import random
from typing import List
from network import Network, run_network, is_sorted, random_network
from evolution import crossover, mutate, tournament_selection

TestCase = List[int]
Parasite = List[TestCase]

def random_test_case(n_wires: int) -> TestCase:
    return [random.randint(0, 1) for _ in range(n_wires)]

def random_parasite(n_wires: int, parasite_size: int = 10) -> Parasite:
    return [random_test_case(n_wires) for _ in range(parasite_size)]

def host_fitness(host: Network, parasites: List[Parasite]) -> float:
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
    child = [case.copy() for case in parasite]

    for case in child:
        for i in range(len(case)):
            if random.random() < mutation_rate:
                case[i] = 1 - case[i]

    return child

def crossover_parasite(p1: Parasite, p2: Parasite) -> Parasite:
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
):
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
        # each host is evaluated against a small sample of parasites
        host_fitnesses = []
        for host in host_population:
            sampled_parasites = random.sample(
                parasite_population,
                min(5, len(parasite_population))
            )
            score = host_fitness(host, sampled_parasites)
            # small length penalty
            score -= 0.01 * len(host)
            host_fitnesses.append(score)

        # each parasite is evaluated against a small sample of hosts
        parasite_fitnesses = []
        for parasite in parasite_population:
            sampled_hosts = random.sample(
                host_population,
                min(5, len(host_population))
            )
            score = parasite_fitness(parasite, sampled_hosts)
            parasite_fitnesses.append(score)

        # best host in this generation
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

        # evolve hosts
        new_hosts = [gen_best_host.copy()]   # elitism
        while len(new_hosts) < host_population_size:
            p1 = tournament_selection(host_population, host_fitnesses)
            p2 = tournament_selection(host_population, host_fitnesses)
            child = crossover(p1, p2)
            child = mutate(child, n_wires)
            new_hosts.append(child)

        # evolve parasites
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