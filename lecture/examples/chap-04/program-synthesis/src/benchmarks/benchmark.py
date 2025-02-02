def generate_counterexamples(examples, n):
    counterexamples = [i for i in range(n) if n not in examples]
    return counterexamples

def generate_dataset(examples, n):
    dataset = []
    for i in range(n):
        if i in examples:
            dataset.append((i, 1))
        else:
            dataset.append((i, 0))
    return dataset