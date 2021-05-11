from typing import List, Tuple

def combined(l: List[int], threshold: int):
    num_of_combinations = 0
    num: int = 0
    combinations: List[Tuple] = []
    for i in range(len(l)):
        for j in range(1, len(l) - i + 1):
            if sum(l[i:i + j]) / j >= threshold:
                num += 1
                combinations.append(tuple(l[i:i + j]))
            num_of_combinations += 1
    return num, combinations, num_of_combinations

def evaluate(l: List[int], threshold: int):
    num, combinations, num_of_combs = combined(l, threshold)
    print(f'''
Combinations That Meet Threshold:
{combinations}

Maximum Number Of Shoffee (Without Treshold):
{num_of_combs}

Maximum Number Of Shoffee (With Treshold):
{num}''')