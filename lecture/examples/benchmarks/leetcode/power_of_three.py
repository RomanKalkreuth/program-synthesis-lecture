import random
import math

examples = [1, 3, 9, 27, 81, 243, 729, 2187, 6561, 19683, 59049,
            177147, 531441, 1594323, 4782969, 14348907, 43046721,
            129140163, 387420489, 1162261467, 3486784401]

def generate_dataset(n, m):
    powers = [int(math.pow(3,i)) for i in range(n + 1)]
    dataset = [(power, 1) for power in powers]
    max = 2 ** n
    for i in range(m - len(powers)):
        rand = random.randint(-max, max - 1)
        if rand not in dataset:
            dataset.append((rand, 0))
    dataset.append((0,0))
    random.shuffle(dataset)
    return dataset