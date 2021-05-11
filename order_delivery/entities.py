# Strong Typing Dependency
from typing import List

# Represent graph using list of adjacency lists


class Graph():
    adj: List[List[int]]

    def __init__(self, nodes: int = 0):
        self.adj = [[] for _ in range(nodes)]

    def addEdge(self, fr: int, to: int) -> None:
        self.adj[fr - 1].append(to - 1)
        self.adj[to - 1].append(fr - 1)

    def print(self) -> None:
        print("Adjacency Lists:")
        for i, adj in enumerate(self.adj):
            print(i, adj, sep=': ')


class Warehouse():
    stock: int
    fee: int
    index: int

    def __init__(self, stock: int, fee: int, index: int):
        self.stock = stock
        self.fee = fee
        self.index = index


class Customer():
    orders: int
    index: int

    def __init__(self, orders: int, index: int):
        self.orders = orders
        self.index = index
