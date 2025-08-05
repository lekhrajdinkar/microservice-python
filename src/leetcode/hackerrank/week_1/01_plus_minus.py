#!/bin/python3

"""
Given an array of integers, calculate the ratios of its elements that are positive, negative, and zero.
Print the decimal value of each fraction on a new line with  places after the decimal.

Note: This challenge introduces precision problems.
The test cases are scaled to six decimal places, though answers with absolute error of up to  are acceptable.

Example

There are 5 elements, two positive, two negative and one zero. Their ratios are ,  and . Results are printed as:

0.400000
0.400000
0.200000
"""

def plusMinus(arr):
    length = len(arr)
    if length < 0 or length > 100:
        return
    positive = 0
    negative = 0
    zero = 0
    for i in range(length):
        if arr[i] > 0 and arr[i] <= 100:
            positive += 1
        elif arr[i] >= -100 and arr[i] < 0 :
            negative += 1
        else:
            zero += 1

    print(f"{positive/length:.6f}" , f"{negative/length:.6f}", f"{zero/length:.6f}", sep = '\n')


if __name__ == '__main__':
    n = int(input('enter n : ').strip())
    arr = list(map(int, input('enter array : ').rstrip().split()))
    #print(n, arr, type(n), type(arr))
    plusMinus(arr)