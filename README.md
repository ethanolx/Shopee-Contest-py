# Shopee Challenge

|                   |   |                       |
|-------------------|---|-----------------------|
|   Author          | : |   Ethan Tan Wee En    |
|   Languages       | : |   Python (py)         |
|   Date            | : |   May 2021            |

## File Structure

```
    Shopee ---- divider ---- algo.py
            |
            |-- order_delivery ---- algo.py
            |                   `-- entities.py
            |
            |-- shoffee ---- algo.py
            |
            |-- tanam ---- algo.py
            |
            |-- .gitignore
            |-- brief.pdf
            |-- main.py
            `-- README.md
```

## Entry Point

Algorithms performed on sample data: `main.py`

## Algorithms

### Tanam

*   Algorithm:
    1. For each day, find the best value for each move (return to left, go across, return to right) - O(c)
    2. For each subsequent day, find the best path to reach each of the left and right positions - O(d)
    3. Compare the values of the most optimal left and right pathways - O(1)
*   Time Complexity: O(c + d)
*   Space Complexity: O(cd)

where c is the number of cells and d is the number of days

### Shoffee

*   Algorithm:
    1. Iterate through each of the combinations, check if average value meets the threshold - O(n<sup>2</sup>)
*   Time Complexity: O(n<sup>2</sup>)
*   Space Complexity: O(n)

where n is the number of different coffee bean flavours

### Order Delivery

Algorithm:
1. Use BFS to find shortest routes from each order city to each warehouse
2. Extract fee matrix using the fees and minimum distances
3. Allocate warehouses to order cities, assuming unlimited stock
4. Reallocate warehouses to order cities to accommodate limited stock
5. Calculate final costs

### Divider

*   Algorithm:
    1. Assume unlimited dividers initially - O(1)
    2. Remove dividers based on minimum noise value gained until required dividers are available - O(e<sup>2</sup> - d<sup>2</sup>)
*   Time Complexity: O(e<sup>2</sup> - d<sup>2</sup>)
*   Space Complexity: O(e)

where d is the number of dividers and e is the number of engineers