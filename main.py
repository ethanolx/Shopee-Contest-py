from termcolor import colored

# TANAM #
def tanam_():
    from tanam.algo import tanam_evaluate

    print(colored('TANAM', 'blue'))

    tanam_evaluate(cells=[[-9, -8, 1, 2, 3]])
    tanam_evaluate(cells=[[1, 4, -5], [-1, -9, 100]])
    tanam_evaluate(cells=[[1, 4, -5], [-1, -1, 100]])


# SHOFFEE #
def shoffee_():
    from shoffee.algo import shoffee_evaluate

    print(colored('SHOFFEE', 'blue'))

    shoffee_evaluate(expectations=[1, 3, 4], threshold=3)
    shoffee_evaluate(expectations=[1, 1, 4, 5, 1, 4], threshold=3)


# ORDER DELIVERY #
def order_delivery_():
    from order_delivery.entities import Graph, Warehouse, Customer
    from order_delivery.algo import order_delivery_evaluate

    print(colored('ORDER DELIVERY', 'blue'))

    # Given Sample
    graph = Graph(8, [
        (1, 2),
        (1, 3),
        (2, 3),
        (3, 4),
        (4, 5),
        (5, 6),
        (5, 7),
        (5, 8),
        (4, 6),
        (3, 7),
        (7, 8)
    ])

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
    order_delivery_evaluate(graph=graph, warehouses=warehouses, orders=orders)
    order_delivery_evaluate(graph=graph, warehouses=warehouses_2, orders=orders_2)
    order_delivery_evaluate(graph=graph, warehouses=warehouses_3, orders=orders_2)

    # Another Sample
    graph2 = Graph(5, [
        (1, 2),
        (1, 3),
        (2, 3),
        (2, 5),
        (4, 5)
    ])

    warehouses2 = [
        Warehouse(1, 10, 1),
        Warehouse(1, 2, 0),
    ]

    orders2 = [
        Customer(1, 2),
        Customer(1, 3)
    ]

    order_delivery_evaluate(graph=graph2, warehouses=warehouses2, orders=orders2)


# DIVIDER #
def divider_():
    from divider.algo import divider_evaluate

    print(colored('DIVIDER', 'blue'))

    divider_evaluate(engineers=[1, 3, 2, 4], dividers=1)


# RUN #
algorithms = [tanam_, shoffee_, order_delivery_, divider_]
for algo in algorithms:
    print(colored('\n================\n', 'green'))
    algo()