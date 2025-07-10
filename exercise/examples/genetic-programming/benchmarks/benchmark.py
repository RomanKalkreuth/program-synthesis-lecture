
import numpy as np

class SRBenchmark:

    @staticmethod
    def koza1(x):
        return pow(x, 4) + pow(x, 3) + pow(x, 2) + x

    @staticmethod
    def koza2(x):
        return pow(x, 5) - 2 * pow(x, 3) + x

    @staticmethod
    def koza3(x):
        return pow(x, 6) - 2 * pow(x, 4) + pow(x, 2)

    @staticmethod
    def random_set(min, max, n, objective, dim=1):
        def random_samples(min, max, n, dim=1):
            assert min < max
            samples = []

            for i in range(0, dim):
                sample = (max - min) * np.random.random_sample(n) + min
                samples.append(sample)

            return np.stack(samples, axis=1)

        samples = random_samples(min, max, n, dim)
        values = [objective(point) for point in samples]

        return samples, np.array(values)

class LSBenchmark:

    @staticmethod
    def majority(inputs):
        return 1 if sum(inputs) >= (len(inputs) / 2) else 0

    @staticmethod
    def truth_table(n, objective):
        inputs = [list(map(lambda x: int(x), bin(i)[2:].zfill(n))) for i in range(0, 2 ** n)]
        outputs = [objective(ip) for ip in inputs]
        return inputs, outputs

class PSBenchmark:

    @staticmethod
    def generate_counterexamples(examples, n):
        counterexamples = [i for i in range(n) if n not in examples]
        return counterexamples

    @staticmethod
    def generate_dataset(examples, n):
        dataset = []
        for i in range(n):
            if i in examples:
                dataset.append((i, 1))
            else:
                dataset.append((i, 0))
        return dataset