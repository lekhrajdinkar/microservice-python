"""
Given a square matrix, calculate the absolute difference between the sums of its diagonals.
For example, the square matrix  is shown below:
1 2 3
4 5 6
9 8 9
"""

#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'diagonalDifference' function below.
#
# The function is expected to return an INTEGER.
# The function accepts 2D_INTEGER_ARRAY arr as parameter.
#

def diagonalDifference(arr):
    n = len(arr)
    sum1 = 0
    sum2 = 0

    for i in range(n):
        sum1 += arr[i][i]               # Primary diagonal
        sum2 += arr[i][n - 1 - i]       # Secondary diagonal

    return abs(sum1 - sum2)


if __name__ == '__main__':
    n = 3
    arr = []
    arr.append(list(map(int, "11 2 4".rstrip().split())))
    arr.append(list(map(int, "4 5 6".rstrip().split())))
    arr.append(list(map(int, "10 11 -12".rstrip().split())))

    result = diagonalDifference(arr)
    print(result)

