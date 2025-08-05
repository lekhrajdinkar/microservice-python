"""
heapq is a Python standard library module that provides an implementation of the heap queue algorithm,
also known as a priority queue.
It is based on a binary min-heap

The smallest element is always at index 0.

For every node i,
    heap[i] <= heap[2*i + 1] (left child)
    heap[i] <= heap[2*i + 2] (right child)

        1        <- index 0 (root)
       / \
      3   8      <- indices 1, 2
     / \
    5   4        <- indices 3, 4

Index:    0  1  2  3  4
Values:   1  3  8  5  4

✅ When to Use heapq ??
| Use Case                                 | Why `heapq` Helps                                  |
| ---------------------------------------- | -------------------------------------------------- |
| **1. Priority Queue**                    | Automatically processes items by priority          |
| **2. Always get min/max fast**           | `heap[0]` is always the smallest (min-heap)        |
| **3. Top-k smallest/largest**            | Faster than sorting (`O(n log k)` vs `O(n log n)`) |
| **4. Merge multiple sorted lists**       | `heapq.merge()` handles sorted streams efficiently |
| **5. Streaming median, percentile**      | Process large/streamed data in chunks              |
| **6. Graph algorithms (e.g., Dijkstra)** | Uses min-heap for efficient shortest path          |

"""

import heapq

# Create a min-heap
nums = [5, 3, 8, 1, 4]
heapq.heapify(nums)
print(nums)  # [1, 3, 8, 5, 4] -> heap structure

# Push an element
heapq.heappush(nums, 2)
print(nums)  # [1, 2, 8, 5, 4, 3]

# Pop the smallest element
smallest = heapq.heappop(nums)
print(smallest)  # 1
print(nums)      # [2, 3, 8, 5, 4]

# Get 3 smallest elements (without modifying original)
top3 = heapq.nsmallest(3, nums)
print(top3)  # [2, 3, 4]

low3= heapq.nsmallest(3, nums)
print(low3)
