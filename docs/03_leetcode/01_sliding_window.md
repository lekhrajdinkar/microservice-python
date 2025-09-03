## concept
-  to solve array or string problems 
- that involve **contiguous subarrays or substrings.**
    - without changing the order and without skipping any elements. 
- Instead of recalculating things repeatedly for every subarray, 
- slide a "window" across the input, **reusing previous computations** to reduce time complexity.
- core idea : 
    - Maintain a window (range of elements) 
    - and slide it (i.e., grow/shrink or move right) to process the array efficiently.

## example
- Maximum/minimum sum of subarray of size k 
- Longest substring with given conditions 
- Count of subarrays satisfying conditions 
- Average of subarrays

## strategies

| # | Strategy Type                            | Concept                                                                    | When to Use                                                               | Example Problem (Simplified)                                                                                              |
| - | ---------------------------------------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| 1 | **Fixed-Size Window**                    | Maintain a window of size `k`. Add next element, remove oldest.            | When the window size is fixed (e.g., max sum of size `k`).                | 🧩 Max sum of subarray size `k` <br> `nums = [1, 2, 3, 4, 5], k = 3 → max = 12` <br> 👉 Use `sum(nums[i:i+k])` and slide. |
| 2 | **Variable-Size Window (Grow & Shrink)** | Expand right until invalid, then shrink left until valid.                  | When conditions must be satisfied dynamically (e.g., longest substring).  | 🧩 Longest substring with ≤ 2 distinct chars <br> `s = "eceba", k = 2 → "ece"` <br> 👉 Use hashmap to count chars.        |
| 3 | **Sliding Window with Frequency Count**  | Maintain a frequency map for elements inside the window.                   | Useful when needing to count or track elements (e.g., permutations).      | 🧩 Check if string has any permutation of another <br> `s1 = "ab", s2 = "eidbaooo"` → ✅ <br> 👉 Compare char counts.      |
| 4 | **Max/Min in Window**                    | Use deque to maintain max/min in current window efficiently.               | When finding max/min of each window (monotonic queue).                    | 🧩 Max in all windows of size `k` <br> `nums = [1,3,-1,-3,5,3,6,7], k = 3` <br> 👉 Use deque to track indices.            |
| 5 | **Dynamic Window with Condition**        | Use window and condition to count valid subarrays/strings dynamically.     | Count # of valid subarrays that meet a property.                          | 🧩 Count subarrays with at most `k` odd numbers <br> `nums = [1,1,2,1,1], k = 3 → 6` <br> 👉 Two-pointer approach.        |
| 6 | **Two Pointers with Early Exit**         | Similar to sliding window, but return early or stop on first valid window. | When you want the **first** or **minimum** window satisfying constraints. | 🧩 Minimum window substring containing all chars <br> `s = "ADOBECODEBANC", t = "ABC"` → `"BANC"`                         |


## common problems

| Problem                                                                               | Description                               |
|---------------------------------------------------------------------------------------| ----------------------------------------- |
| [643](https://leetcode.com/problems/maximum-average-subarray-i/)                      | Max average of subarray size `k`          |
| [567](https://leetcode.com/problems/permutation-in-string/)                           | Permutation in string                     |
| [3](https://leetcode.com/problems/longest-substring-without-repeating-characters/) ✅  | Longest substring without repeats         |
| [76](https://leetcode.com/problems/minimum-window-substring/)                         | Min window substring with all chars       |
| [1004](https://leetcode.com/problems/max-consecutive-ones-iii/)                       | Max consecutive 1s with at most `k` flips |
