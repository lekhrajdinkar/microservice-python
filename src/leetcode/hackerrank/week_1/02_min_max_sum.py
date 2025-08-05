def miniMaxSum(arr):
    arr.sort()
    min=0
    for i in range(0,4):
        min = min + arr[i]

    max = 0
    for i in range(1,5):
        max = max + arr[i]

    print(min, max)

if __name__ == '__main__':
    arr = list(map(int, input().rstrip().split()))
    miniMaxSum(arr)
