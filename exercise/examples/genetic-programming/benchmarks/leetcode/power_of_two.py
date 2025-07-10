# https://leetcode.com/problems/power-of-two/

import random
import math

# Testcases from Leetcode
testcases = [(0, 0), (1, 1), (-1, 0), (16, 1), (65536, 1)]
examples = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024,
            2048, 4096, 8192, 16384, 32768, 65536, 131072,
            262144, 524288, 1048576]

# https://github.com/hongxiaolong/leetcode/blob/master/Python/power_of_two.py
def isPowerOfTwo(n):
    return n > 0 and bin(n).count('1') == 1

def generate_dataset(n, m):
    powers = [int(math.pow(2,i)) for i in range(n + 1)]
    dataset = [(power, 1) for power in powers]
    max = 2 ** n
    for i in range(m - len(powers)):
        rand = random.randint(-max, max - 1)
        if rand not in dataset:
            dataset.append((rand, 0))
    dataset.append((0,0))
    random.shuffle(dataset)
    return dataset
