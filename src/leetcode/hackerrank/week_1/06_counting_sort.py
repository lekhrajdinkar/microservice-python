def countingSort(arr):
    if not arr:
        return []

    max_val = max(arr)
    min_val = min(arr)
    range_size = max_val - min_val + 1

    # Step 1: Count frequencies
    count = [0] * range_size
    for num in arr:
        count[num - min_val] += 1  # ◀️

    # Step 2: Reconstruct sorted array
    output = []
    for i in range(range_size):
        output.extend([i + min_val] * count[i]) # ◀️

    return output


if __name__ == '__main__':
    result = countingSort(list([1,1,3,2,1]))
    print(result)

