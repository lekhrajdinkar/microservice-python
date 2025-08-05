def tuple_demo():
    # 1. Create tuples
    t1 = (1, 2, 3)
    t2 = 4, 5, 6               # parentheses optional
    t3 = ()                   # empty tuple
    t4 = (7,)                 # single-element tuple (comma required) ⬅️

    print("t1:", t1)
    print("t4 single element tuple:", t4)

    # 2. Access elements (indexing, slicing)
    print("t1[0]:", t1[0])
    print("t2 slice:", t2[1:])

    # 3. Tuple unpacking ⬅️
    a, b, c = t1
    print("Unpacked:", a, b, c)

    # 4. Immutability (tuples cannot be modified)
    try:
        t1[0] = 10
    except TypeError as e:
        print("Immutability error:", e)

    # 5. Nesting tuples ⬅️
    nested = (t1, t2, ("a", "b"))
    print("Nested tuple:", nested)

    # 6. Using tuples as dict keys (hashable)
    d = {t1: "tuple key value"}
    print("Dict lookup with tuple key:", d[t1])

    # 7. Returning multiple values from a function (tuple packing/unpacking)
    def min_max(values):
        return min(values), max(values)

    result = min_max([10, 5, 7, 2]) # ⬅️
    print("Min, Max:", result)

    # 8. Swap variables using tuple unpacking  ⬅️
    x, y = 1, 2
    x, y = y, x
    print("Swapped:", x, y)

    # 9. Performance (tuples are faster than lists for fixed data)
    import timeit
    print("Tuple creation time:", timeit.timeit("(1,2,3,4,5)", number=1000000))
    print("List creation time:", timeit.timeit("[1,2,3,4,5]", number=1000000))

    # 10. Iterate over tuple
    for item in t1:
        print("Item:", item)

    # 11. Count and index
    print("Count of 2 in t1:", t1.count(2))
    print("Index of 3 in t1:", t1.index(3))
