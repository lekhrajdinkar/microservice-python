#
# Complete the 'lonelyinteger' function below.
#
# The function is expected to return an INTEGER.
# The function accepts INTEGER_ARRAY a as parameter.
#

def lonelyinteger(a):
    tracker :dict = {}
    for  i in set(a):
        tracker[i] = a.count(i)

    print(tracker)
    min_item = min(tracker.items(), key=lambda x: x[1])
    return min_item[0]

if __name__ == '__main__':
    result = lonelyinteger(list([1,1,2,2,3]))
    print(result)

