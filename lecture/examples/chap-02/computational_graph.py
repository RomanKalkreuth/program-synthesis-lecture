import copy
import random
from abc import abstractmethod, ABC
from dataclasses import dataclass, field
from config import GraphConfig
from src.chap02.functions import ADD, MUL, SUB, DIV
from symbols import Symbol, Var, Const

@dataclass
class Vertex:
    symbol: Symbol
    index: int
    source: list = field(default_factory=lambda: [])
    dest: list = field(default_factory=lambda: [])

class Graph(ABC):

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def add_vertex(self, *args):
        pass

    @abstractmethod
    def remove_vertex(self, v):
        pass

    @abstractmethod
    def add_edge(self, v1, v2):
        pass

    @abstractmethod
    def remove_edge(self, v1, v2):
        pass

    @abstractmethod
    def contains_edge(self, v1, v2):
        pass

    @abstractmethod
    def has_edge(self, v):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def path(self, *args):
        pass

class ComputationalGraph(Graph):

    @abstractmethod
    def predict(self, observation):
        pass

class AdjacencyList(ComputationalGraph):

    def __init__(self, config_: GraphConfig):
        self._vertices = []
        self._edges = []
        self._sinks = []
        self._sources = []
        self._paths = []
        self._config = config_

    def add_vertex(self, symbol):
        self._vertices.append(symbol)
        self._edges.append(list())

    def remove_vertex(self, vertex):
        self._vertices.pop(vertex)
        self._edges.pop(vertex)

    def add_edge(self, v1, v2):
        if len(self._vertices) >= v1:
            self._edges[v1].append(v2)
        else:
            self._edges.append([v2])

    def remove_edge(self, v1, v2):
        if len(self._vertices) >= v1:
            for index, edge in enumerate(self._edges[v1]):
                if edge == v2:
                    self._edges[v1].remove(index)
                    break

    def contains_edge(self, v1, v2):
        if len(self._vertices) >= v1:
            for index, edge in enumerate(self._edges[v1]):
                if edge == v2:
                    return True
        return False

    def has_edge(self, v):
        return len(self.edges[v]) > 0

    def path(self, v, path=None):
        if path is None:
            path = []
        arity = self._vertices[v].arity
        if arity is not None:
            for i in range(arity):
                excl = [e[0] for e in path] + [v]
                choices = [v for v in range(0, len(self._vertices) - 1) if v not in excl]
                v_next = random.choice(choices)
                self.add_edge(v, v_next)
                path.append((v, v_next))
                self.path(v_next, path)
        else:
            if v not in self._sources:
                self._sources.append(v)
        return path

    def decode(self):
        self._paths.clear()
        edges = copy.deepcopy(self._edges)
        for v in self._sinks:
            path = self.walk(v, edges)
            self._paths.append(path)

    def walk(self, vertex, edges, path=None):
        if path is None:
            path = {}
        arity = self._vertices[vertex].arity
        if arity is not None:
            for i in range(arity):
                edge = edges[vertex].pop(0)
                if vertex not in path.keys():
                    path[vertex] = [edge]
                else:
                    path[vertex] += [edge]
                self.walk(edge, edges, path)
        else:
            path[vertex] = []
        return path

    def print_vertices(self):
        print("Vertices: ")
        for index, label in enumerate(self._vertices):
            print("Vertex #" + str(index) + " - Label: " + str(label))

    def print_edges(self):
        print("Edges: ")
        for index, edges in enumerate(self._edges):
            if len(edges) > 0:
                print("Vertex #" + str(index) + " : ", end="")
                print(edges)

    def print_sinks(self):
        print("Outputs: ", end=" ")
        print(self._sinks)

    def print_sources(self):
        print("Inputs: ", end=" ")
        print(self._sources)

    def print_paths(self):
        print("Paths: ")
        for path in self._paths:
            print(path)

    def clear(self):
        self._vertices.clear()
        self._edges.clear()

    def print(self):
        self.print_vertices()
        self.print_edges()

    @property
    def sinks(self):
        return self._sinks

    @property
    def vertices(self):
        return self._vertices

    @property
    def edges(self):
        return self._edges


class SymbolicGraph(AdjacencyList):

    def __init__(self, config_: GraphConfig):
        super().__init__(config_)
        self.init()

    def init(self):
        num_nodes = random.randint(self._config.min_nodes, self._config.max_nodes)

        for i in range(num_nodes):
            if random.random() > self._config.symbol_ratio:
                rand_symbol = random.choice(self._config.non_terminals)
            else:
                rand_symbol = random.choice(self._config.terminals)
            self.add_vertex(rand_symbol)

        for i in range(self._config.num_outputs):
            rand_vertex = random.randint(0, len(self._vertices) - 1)
            self._sinks.append(rand_vertex)
            path = self.path(rand_vertex)
            self._paths.append(path)

    def predict(self, observation):

        def predict_path(path: dict, observation: list, vertex: int):
            symbol = self._vertices[vertex]

            if isinstance(symbol, Var):
                return observation[symbol()]
            elif isinstance(symbol, Const):
                return symbol()
            else:
                edges = path[vertex]
                args = []
                for edge in edges:
                    args.append(predict_path(path, observation, edge))
                return symbol(*args)

        if self._paths is None:
            self.decode()

        predictions = []

        for i, path in enumerate(self._paths):
            sink = self._sinks[i]
            prediction = predict_path(path, observation, sink)
            predictions.append(prediction)

        return predictions

functions = [ADD, MUL, SUB, DIV]
terminals = [Const("c0", 0), Const("c1", 1),
             Var("v0", 0), Var("v1", 1)]

graph_config = GraphConfig(non_terminals=functions,
                          terminals=terminals,
                          operators=None,
                          min_nodes=10,
                          max_nodes=20,
                          num_inputs=2,
                          num_outputs=3)

SymbolicGraph(config_=graph_config)