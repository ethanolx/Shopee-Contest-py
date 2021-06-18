from typing import List, Tuple, Union
import numpy as np
import pandas as pd

def get_max_gain(l: List[int], from_right: bool = False):
    tmp = l.copy()
    if from_right:
        tmp.reverse()
    steps = 0
    full_steps = 0
    max_gain = 0
    sum_vals = 0
    for i, val in enumerate(tmp):
        sum_vals += val
        full_steps += 1
        if sum_vals > max_gain:
            max_gain = sum_vals
            steps = i + 1
    return (max_gain, steps), (sum_vals, full_steps)

def get_combination_matrix(l: List[List[int]]):
    right_moves = []
    right_steps = []
    across_moves = []
    across_steps = []
    left_moves = []
    left_steps = []
    for day in l:
        (r_val, r_steps), (a_val, a_steps) = get_max_gain(day)
        (l_val, l_steps), _ = get_max_gain(day, from_right=True)
        right_moves.append(r_val)
        right_steps.append(r_steps)
        across_moves.append(a_val)
        across_steps.append(a_steps)
        left_moves.append(l_val)
        left_steps.append(l_steps)
    return pd.DataFrame(
        data=np.array([right_moves, right_steps, across_moves, across_steps, left_moves, left_steps]).T,
        columns=['Right Move', 'Right Steps', 'Across', 'Across Steps', 'Left Move', 'Left Steps']
    )

def combined(l: List[List[int]]):
    movement_matrix = get_combination_matrix(l)
    end_l_path = [f'{movement_matrix.iloc[0, 1]} >']
    end_r_path = [f'{movement_matrix.iloc[0, 3]} >>']
    current_end_left_val = movement_matrix.loc[0, 'Right Move']
    current_end_right_val = movement_matrix.loc[0, 'Across']

    for i in range(1, len(l)):
        move_right_val = movement_matrix.loc[i, 'Right Move']
        move_across_val = movement_matrix.loc[i, 'Across']
        move_left_val = movement_matrix.loc[i, 'Left Move']

        # Temporary variables
        next_end_left_val = current_end_left_val
        next_end_right_val = current_end_right_val
        end_l_path_tmp = end_l_path.copy()
        end_r_path_tmp = end_r_path.copy()

        # Evaluate end left combinations first
        if current_end_left_val + move_right_val >= current_end_right_val + move_across_val:
            next_end_left_val = current_end_left_val + move_right_val
            end_l_path_tmp.append(f'{movement_matrix.iloc[i, 1]} >')
        else:
            next_end_left_val = current_end_right_val + move_across_val
            end_l_path_tmp = end_r_path.copy()
            end_l_path_tmp.append(f'<< {movement_matrix.iloc[i, 3]}')

        if current_end_right_val + move_left_val >= current_end_left_val + move_across_val:
            next_end_right_val = current_end_right_val + move_left_val
            end_r_path_tmp.append(f'< {movement_matrix.iloc[i, 5]}')
        else:
            next_end_right_val = current_end_left_val + move_across_val
            end_r_path_tmp = end_l_path.copy()
            end_r_path_tmp.append(f'{movement_matrix.iloc[i, 3]} >>')

        current_end_left_val = next_end_left_val
        current_end_right_val = next_end_right_val
        end_l_path = end_l_path_tmp.copy()
        end_r_path = end_r_path_tmp.copy()

    if current_end_left_val == current_end_right_val:
        return current_end_left_val, [end_l_path, end_r_path], movement_matrix
    if current_end_left_val > current_end_right_val:
        return current_end_left_val, [end_l_path], movement_matrix
    else:
        return current_end_right_val, [end_r_path], movement_matrix

def tanam_evaluate(cells: List[List[int]]):
    max_gain, paths_taken, movement_matrix = combined(cells)
    print(f'''
Movement Matrix:
{movement_matrix}

Maximum Health Gain:
{max_gain}

Corresponding Paths:
{list(map(lambda x: ' ... '.join(x), paths_taken))}''')