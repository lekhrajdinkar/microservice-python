"""
Input: nums = [2,3,1,1,4]
Output: true
Explanation:
- Start at index 0 (value = 2). Can jump up to 2 steps.
- Jump to index 2 (value = 1). Can jump up to 1 step.
- Jump to index 3 (value = 1). Can jump up to 1 step.
- Jump to index 4 (last index). Success!
"""
from operator import truediv


class Solution:
    def canJump(self, nums) -> bool:
        n=len(nums)
        i=0
        def jump(i):
            old_i = i
            max_step=nums[i]

            new_i = min(old_i+max_step, n-1)
            #for x in range(old_i, new_i):
            # todo : add greedy

            print(f'old_index: {old_i}  | move by max_step count: {max_step} | new_index: {new_i} | reached at  {nums[:new_i+1]}')
            if new_i == n-1:
                return True
            elif old_i == new_i:
                return False

            return jump(new_i)

        return True if jump(0) else False


print(Solution().canJump([2,3,1,1,4]))
print(Solution().canJump([2,5,0,0]))

# Leet code 6 🚫
# Zig Zag
"""
['', '', '']
['l', '', '']
['l', 'e', '']
['l', 'e', 'k']
['l', 'eh', 'k']
['lr', 'eh', 'k']
['lr', 'eha', 'k']
['lr', 'eha', 'kj']
['lr', 'ehad', 'kj']
['lri', 'ehad', 'kj']
['lri', 'ehadn', 'kj']
['lri', 'ehadn', 'kjk']
['lri', 'ehadna', 'kjk']
"""
class Solution6:
    def convert(self, s: str, numRows: int) -> str:
        if numRows == 1 or numRows >= len(s):
            return s

        rows = [''] * numRows
        cur_row = 0
        going_down = False

        for char in s:
            print(rows)
            rows[cur_row] += char
            if cur_row == 0 or cur_row == numRows - 1:
                going_down = not going_down
            cur_row += 1 if going_down else -1

        return ''.join(rows)

print(Solution6().convert('lekhrajdinkar',3))

# 28 https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/?envType=study-plan-v2&envId=top-interview-150
class Solution28:
    def strStr(self, haystack: str, needle: str) -> int:
        n1 = len(needle)
        n2 = len(haystack)

        if needle == haystack:
            return 0
        print(f'loop {n2-n1} time')
        for i in range(n2-n1+1):
            print(f'haystack: {haystack[i:i+n1]} == needle: {needle}')
            if haystack[i:i+n1] == needle:
                return i

        return -1

print('#28 ',Solution28().strStr('leetcode','code'))


# 125 https://leetcode.com/problems/valid-palindrome/?envType=study-plan-v2&envId=top-interview-150
class Solution125:
    def isPalindrome(self, s: str) -> bool:
        if s == " ": return True

        filtered = "".join(c for c in s if c.isalnum())
        reversed = filtered[::-1]
        print(s,filtered,reversed)
        return filtered.lower() == reversed.lower()

print('#125 ',Solution125().isPalindrome("A man, a plan, a canal: Panama"))