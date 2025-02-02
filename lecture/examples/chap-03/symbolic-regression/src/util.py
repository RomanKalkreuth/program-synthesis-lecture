import matplotlib.pyplot as plt

from inspect import signature


def get_variables_from_terminals(terminals):
    variables = []
    for terminal in terminals:
        if type(terminal) == str:
            variables.append(terminal)
    return variables


ELBOW = "└──"
PIPE = "│  "
TEE = "├──"
BLANK = "   "


def print_tree_vertically(tree, term="", left=False, right=False):
    if tree.symbol is None:
        return

    prefix = ""

    if right or tree.parent is None:
        prefix += ELBOW
    elif left and tree.parent.right is None:
        prefix += ELBOW
    elif left:
        prefix += TEE

    print("%s%s%s" % (term, prefix, tree.symbol))

    appendix = (PIPE if left and tree.parent.right is not None else BLANK)

    if tree.left is not None:
        print_tree_vertically(tree.left, term + appendix, left=True, right=False)
    if tree.right is not None:
        print_tree_vertically(tree.right, term + appendix, left=False, right=True)


def plot_xy(samples, prediciton):
    x = [sample[0] for sample in samples]
    y = [p for p in prediciton]
    plt.plot(x, y, 'o')
    plt.show()


def arity(function):
    parameters = signature(function).parameters
    return len(parameters)
