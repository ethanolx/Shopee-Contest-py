# Import Dependencies
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Union, cast
from .entities import Graph, Warehouse, Customer

# Extract element-wise attributes from a list of objects
def get_attrs(ls: Union[List[Warehouse], List[Customer]], attr: str = "index") -> List:
    return list(map(lambda w: getattr(w, attr), ls))

# get_route_matrix subfunctions -> bfs, bfs_wrapper, get_shortest_routes, convert_dist_dict_to_list
def bfs(g: Graph, queue: List[int], dist_dict: Dict[int, int], dist: int = 0) -> None:
    adj = g.adj
    new_q: List[int] = []
    for i in queue:
        dist_dict[i] = dist
        for j in adj[i]:
            if j not in queue and j not in new_q and j not in dist_dict.keys():
                new_q.append(j)
    if len(new_q) > 0:
        bfs(g, new_q, dist_dict=dist_dict, dist=dist + 1)

def bfs_wrapper(g: Graph, root: int) -> Dict[int, int]:
    d = {}
    bfs(g, [root], d)
    return d

def get_shortest_routes(g: Graph, warehouses: List[Warehouse]) -> pd.DataFrame:
    w_indices: List[int] = get_attrs(warehouses)
    dist_dict: Dict[int, List[int]] = {}
    for i in w_indices:
        dist_dict[i] = convert_dist_dict_to_list(bfs_wrapper(g=g, root=i))
    return pd.DataFrame(data=dist_dict)  # type: ignore

def convert_dist_dict_to_list(dist_dict: Dict[int, int]) -> List[int]:
    dist_list: List[int] = []
    for i in range(len(dist_dict.keys())):
        dist_list.append(dist_dict[i])
    return dist_list

def drop_irrelevant_cities(route_matrix: pd.DataFrame, orders: List[Customer]) -> pd.DataFrame:
    customer_city_indices: List[int] = get_attrs(orders)
    return route_matrix.iloc[customer_city_indices, :]

# Get relevant route matrix
def get_route_matrix(g: Graph, w: List[Warehouse], o: List[Customer]) -> pd.DataFrame:
    return drop_irrelevant_cities(get_shortest_routes(g, w), o)

# Get relevant fee matrix
def get_fee_matrix(route_matrix: pd.DataFrame, warehouses: List[Warehouse]) -> pd.DataFrame:
    fees: np.ndarray = np.array(get_attrs(warehouses, "fee"))
    return pd.DataFrame(data=route_matrix.values * fees, columns=route_matrix.columns.values, index=route_matrix.index.values)

# absolute_least_cost subfunctions -> get_absolute_highest_quantities, get_next_cheapest
def get_absolute_highest_quantities(alloc: pd.DataFrame, orders: List[Customer], next_cheapest: np.ndarray):
    alloc = alloc.copy()
    alloc[np.array([True for _ in range(alloc.size)]
                      ).reshape(alloc.shape)] = 0
    for row in range(alloc.shape[0]):
        alloc.iloc[row, next_cheapest[row]] = get_attrs(orders, "orders")[
            row]
    return alloc

def get_next_cheapest(fees: np.ndarray, current_index: Union[int, None] = None):
    if current_index is not None:
        current_thresholds = fees[:, current_index].reshape(
            (fees.shape[0], -1))
        masked_arr: np.ndarray = cast(np.ndarray, np.hstack(
            (fees[:, :current_index], fees[:, current_index + 1:])).copy())
        masked_arr[masked_arr < current_thresholds] = fees.max().max() + 1
        argmin = masked_arr.argmin(axis=1)
        argmin[argmin >= current_index] += 1
        return argmin
    else:
        return fees.argmin(axis=1)

# Get total cost of all deliveries
def get_total_cost(alloc: pd.DataFrame, fees: pd.DataFrame):
    return (fees * alloc).sum().sum()

# Get absolute least cost (assuming unlimited stock in each warehouse)
def absolute_least_cost(g: Graph, w: List[Warehouse], o: List[Customer]):
    route_matrix = get_route_matrix(g, w, o)
    fees = get_fee_matrix(route_matrix, w)
    next_cheapest = get_next_cheapest(fees.values)
    alloc = get_absolute_highest_quantities(route_matrix, o, next_cheapest)
    return route_matrix, alloc, fees, get_total_cost(alloc, fees)

# combined subfunctions -> get_overload, determine_best_value, determine_best_action, transfer, reallocate_stocks
def get_overload(alloc: pd.DataFrame, warehouses: List[Warehouse], orders: List[Customer]):
    overload = np.array(get_attrs(warehouses, attr="stock")
                        ) - alloc.sum(axis=0)
    return overload

def determine_best_value(fees: np.ndarray, i: int):
    return get_next_cheapest(fees, current_index=i)

def determine_best_action(fees: np.ndarray, next_cheapest: np.ndarray, i: int):
    l = []
    for j, k in enumerate(next_cheapest.tolist()):
        l.append((fees[j, i] - fees[j, k], j, i, k))
    return l

def transfer(alloc: pd.DataFrame, pos_from: Tuple[int, int], pos_to: Tuple[int, int], qty: int):
    alloc.iloc[pos_from] -= qty  # type: ignore
    alloc.iloc[pos_to] += qty  # type: ignore

def reallocate_stocks(alloc: pd.DataFrame, fees: np.ndarray, warehouses: List[Warehouse], orders: List[Customer], i: int):
    overload = get_overload(alloc, warehouses, orders)
    next_cheapest = determine_best_value(fees, i)
    transfer_vals = determine_best_action(fees, next_cheapest, i)
    transfer_vals = sorted(transfer_vals, key=lambda el: el[0], reverse=True)
    for j in range(alloc.shape[0]):
        next_action = transfer_vals[j]
        __, row, col_from, col_to = next_action
        if alloc.iloc[row, col_from] >= np.abs(overload.iloc[i]):
            transfer(alloc, (row, col_from),
                    (row, col_to), np.abs(overload.iloc[i]))
            break
        else:
            transfer(alloc, (row, col_from), (row, col_to),
                    alloc.iloc[row, col_from]) # type: ignore

# Combined function
def combined(g: Graph, warehouses: List[Warehouse], orders: List[Customer]):
    route_matrix, alloc, fees, least_cost = absolute_least_cost(
        g, warehouses, orders)
    for i in range(len(warehouses)):
        reallocate_stocks(alloc, fees.values, warehouses, orders, i)
    return route_matrix, fees, alloc, least_cost, get_total_cost(alloc, fees)

# Overall function
def order_delivery_evaluate(graph: Graph, warehouses: List[Warehouse], orders: List[Customer]) -> None:
    result = combined(graph, warehouses, orders)
    route_matrix, fee_matrix, alloc_matrix, lowest_cost, lowest_feasible_cost = result
    print(f'''
Route Matrix:
{route_matrix}

Fee Matrix:
{fee_matrix}

Allocation Matrix:
{alloc_matrix}

Least Cost (Unlimited Supply):
${lowest_cost}

Least Cost (Limited Stock in Each Warehouse):
${lowest_feasible_cost}''')
