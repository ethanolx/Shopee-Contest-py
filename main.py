# SHOFFEE #
from shoffee.algo import evaluate as shoffee_evaluate

case1 = [1, 3, 4], 3
case2 = [1, 1, 4, 5, 1, 4], 3

shoffee_evaluate(*case1)
# shoffee_evaluate(*case2)


# ORDER DELIVERY #
from order_delivery.entities import Graph, Warehouse, Customer
from order_delivery.algo import evaluate as order_evaluate

# Given Sample
sample = Graph(8)

sample.addEdge(1, 2)
sample.addEdge(1, 3)
sample.addEdge(2, 3)
sample.addEdge(3, 4)
sample.addEdge(4, 5)
sample.addEdge(5, 6)
sample.addEdge(5, 7)
sample.addEdge(5, 8)
sample.addEdge(4, 6)
sample.addEdge(3, 7)
sample.addEdge(7, 8)

warehouses = [
    Warehouse(12, 5, 0),
    Warehouse(11, 10, 5),
    Warehouse(1, 6, 6)
]

warehouses_2 = [
    Warehouse(1, 6, 6),
    Warehouse(12, 5, 0),
    Warehouse(11, 10, 5)
]

warehouses_3 = [
    Warehouse(11, 10, 5),
    Warehouse(1, 6, 6),
    Warehouse(12, 5, 0)
]

orders = [
    Customer(7, 3),
    Customer(7, 4)
]

orders_2 = [
    Customer(7, 4),
    Customer(7, 3)
]

# Different Orders Yield Varying Results (but with same lowest cost)
order_evaluate(sample, warehouses, orders)
# order_evaluate(sample, warehouses_2, orders_2)
# order_evaluate(sample, warehouses_3, orders_2)

# Yi Chern's Sample
sample2 = Graph(5)

sample2.addEdge(1, 2)
sample2.addEdge(1, 3)
sample2.addEdge(2, 3)
sample2.addEdge(2, 5)
sample2.addEdge(4, 5)

warehouses2 = [
    Warehouse(1, 10, 1),
    Warehouse(1, 2, 0),
]

orders2 = [
    Customer(1, 2),
    Customer(1, 3)
]

# order_evaluate(sample2, warehouses2, orders2)


# DIVIDER #
from divider.algo import evaluate as divider_evaluate

engineers = [1, 3, 2, 4]
dividers = 1

divider_evaluate(engineers, 1)