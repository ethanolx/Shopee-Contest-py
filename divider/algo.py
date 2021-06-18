from typing import List, cast
import numpy as np
import pandas as pd


def combine(l: List[int], gc: List[int], dividers: np.ndarray, i: int):
    new_noise = l[i] + l[i + 1]
    new_count = gc[i] + gc[i + 1]
    new_l = l[:i] + [new_noise] + l[i + 2:]
    new_gc = gc[:i] + [new_count] + gc[i + 2:]
    dividers[dividers > i] -= 1
    return new_l, new_gc


def compare(l: List[int], group_count: List[int], i: int):
    new_noise_level = (l[i] + l[i + 1]) * (group_count[i] + group_count[i + 1])
    old_noise_level = l[i] * group_count[i] + l[i + 1] * group_count[i + 1]
    return new_noise_level - old_noise_level


def remove_divider(dividers: np.ndarray, divider: int):
    return dividers[dividers != divider]


def get_total_noise(l: List[int], gc: List[int]):
    return (np.array(l) * np.array(gc)).sum()


def get_dividers(l: List[int]):
    dividers: List[int] = []
    index = -1
    for group in l[:-1]:
        index += group
        dividers.append(index)
    return dividers


def combined(l: List[int], num_of_dividers: int):
    max_num_of_dividers = len(l) - 1
    dividers: np.ndarray = np.arange(max_num_of_dividers)
    group_count = [1 for _ in range(len(l))]
    for _ in range(max_num_of_dividers - num_of_dividers):
        min_value = None
        targ_divider = None
        for divider in dividers.tolist():
            shift = compare(l, group_count, divider)
            if min_value is None or shift < min_value:
                targ_divider = divider
                min_value = shift
        dividers = remove_divider(dividers, cast(int, targ_divider))
        new_l, new_gc = combine(l, group_count, dividers,
                                cast(int, targ_divider))
        l = new_l
        group_count = new_gc
    return get_total_noise(l, group_count), get_dividers(group_count), np.vstack((np.array(l).reshape((1, -1)), np.array(group_count).reshape((1, -1))))


def divider_evaluate(engineers: List[int], dividers: int):
    lowest_noise_level = sum(engineers)
    total_noise_level, divider_positions, merged_groups = combined(engineers, dividers)
    print(f'''
Group Matrix:
{pd.DataFrame(data=merged_groups, index=['Collective Noise', 'Group Size'])}

Divider Positions (right of 0-based index):
{divider_positions}

Lowest Noise Level (Unlimited Dividers):
{lowest_noise_level}

Lowest Noise Level (Limited Dividers):
{total_noise_level}''')
