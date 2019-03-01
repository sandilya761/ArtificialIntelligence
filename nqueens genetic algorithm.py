import math
import random


def generate_random_layout(dimension):
    return [random.randint(1, dimension) for _ in range(dimension)]


def nCr(n, r):
    assert n > r  # sanity check
    return int(math.factorial(n) / (math.factorial(r) * math.factorial(n - r)))


def fitness(layout):

    max_possible_clashes = nCr(len(layout), 2)
    clashes = 0

    row_clashes = len(layout) - len(set(layout))
    clashes += row_clashes

    # calculate diagonal clashes
    for i in range(len(layout)):
        for j in range(i + 1, len(layout)):
            dx = j - i
            dy = abs(layout[i] - layout[j])
            if(dx == dy):
                clashes += 1

    return max_possible_clashes - clashes


def get_successors(layouts):

    num_samples = len(layouts)

    # get the fitness scores of each board
    fitness_scores = list(map(fitness, layouts))

    # normalize the fitness scores
    fitness_scores = list(map(lambda x: x / sum(fitness_scores), fitness_scores))

    return random.choices(population=layouts, weights=fitness_scores, k=num_samples)


def slice_swap(arr1, arr2):
    assert len(arr1) == len(arr2)

    random_index = random.randint(0, len(arr1) // 2 + 1)
    # print("slice index : ", random_index)
    arr1[:random_index], arr2[:random_index] = arr2[:random_index], arr1[:random_index]


def mutate(arr):
    arr[random.randint(0, len(arr) - 1)] = random.randint(1, len(arr))


def genetic(dimension, num_samples):
    random_layouts = [generate_random_layout(dimension) for _ in range(num_samples)]
    # print("random_layouts : ", random_layouts)
    current_fitness = list(map(fitness, random_layouts))

    iterations = 0
    while (28 not in current_fitness) or iterations < 1000:

        successors = get_successors(random_layouts)
        # print("successors : ", successors)

        # slice the layouts at random index and swap them
        for i in range(dimension // 2):
            slice_swap(successors[i * 2], successors[i * 2 + 1])

        # print("swapped : ", successors)

        # mutate a single element in randomly selected boards
        random_board_numbers = set([random.randint(0, num_samples - 1) for _ in range(random.randint(1, num_samples))])

        for i in random_board_numbers:
            mutate(successors[i])

        # print("mutated : ", successors)
        current_fitness = list(map(fitness, successors))
        iterations += 1

    return successors


if __name__ == '__main__':
    dimension = 8
    final_result = genetic(8, 20)
    print(final_result)
    print(list(map(fitness, final_result)))
