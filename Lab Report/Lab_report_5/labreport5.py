import random

def generate_candidate(size):
    return [random.randint(1, size) for _ in range(size)]

def evaluate(candidate):
    clashes = sum([candidate.count(val) - 1 for val in candidate]) / 2
    n = len(candidate)
    l_diag = [0] * (2 * n)
    r_diag = [0] * (2 * n)
    for idx in range(n):
        l_diag[idx + candidate[idx] - 1] += 1
        r_diag[n - idx + candidate[idx] - 2] += 1
    diag_conflicts = sum([(d - 1) if d > 1 else 0 for d in l_diag]) + \
                     sum([(d - 1) if d > 1 else 0 for d in r_diag])
    return int(best_score - (clashes + diag_conflicts))

def get_probability(individual):
    return evaluate(individual) / best_score

def select_one(group, chances):
    total_chance = sum(chances)
    selection = random.uniform(0, total_chance)
    current = 0
    for person, chance in zip(group, chances):
        if current + chance >= selection:
            return person
        current += chance

def crossover(parent1, parent2):
    point = random.randint(0, len(parent1) - 1)
    return parent1[:point] + parent2[point:]

def alter(individual):
    idx = random.randint(0, len(individual) - 1)
    individual[idx] = random.randint(1, len(individual))
    return individual

def evolve_population(group):
    next_gen = []
    prob_list = [get_probability(ind) for ind in group]
    for _ in range(len(group)):
        p1 = select_one(group, prob_list)
        p2 = select_one(group, prob_list)
        offspring = crossover(p1, p2)
        if random.random() < 0.03:
            offspring = alter(offspring)
        display_individual(offspring)
        next_gen.append(offspring)
        if evaluate(offspring) == best_score:
            break
    return next_gen

def display_individual(indiv):
    print(f"DNA: {indiv} | Score: {evaluate(indiv)}")

def render_board(solution):
    size = len(solution)
    grid = [["." for _ in range(size)] for _ in range(size)]
    for col in range(size):
        grid[size - solution[col]][col] = "Q"
    for line in grid:
        print(" ".join(line))

if __name__ == "__main__":
    n_queens = int(input("How many queens to place? "))
    best_score = (n_queens * (n_queens - 1)) / 2
    pool = [generate_candidate(n_queens) for _ in range(100)]
    gen = 1

    while best_score not in [evaluate(ind) for ind in pool]:
        print(f"\n--- Generation {gen} ---")
        pool = evolve_population(pool)
        top_score = max(evaluate(p) for p in pool)
        print(f"Top Score This Generation: {top_score}")
        gen += 1

    for sol in pool:
        if evaluate(sol) == best_score:
            print(f"\nSuccess in generation {gen - 1}!")
            print("Found a valid solution:")
            display_individual(sol)
            print("\nChessboard layout:")
            render_board(sol)
            break
