"""
Given an array of  distinct integers, transform the array into a zig zag sequence by permuting the array elements.
A sequence will be called a zig zag sequence if the first  elements in the sequence are in increasing order
and the last  elements are in decreasing order, where .
You need to find the lexicographically smallest zig zag sequence of the given array.

[1,2,3,4,5,6,7] input
1 2 3 7 6 5 4 output

"""
def findZigZagSequence(a, n):
    a.sort()
    mid = int((n + 1)/2)

    st = mid - 1
    ed = n - 1
    while(st <= ed):
        a[st], a[ed] = a[ed], a[st]
        st = st + 1
        ed = ed - 1

    for i in range (n):
        if i == n-1:
            print(a[i])
        else:
            print(a[i], end = ' ')
    return


n = 7
a = [1,2,3,4,5,6,7]
findZigZagSequence(a, n)