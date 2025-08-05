## 1 https://leetcode.com/problems/two-sum/description/
class Solution1:
    def twoSum(self, nums, target: int):
        print('--- twoSum ---')
        n = len(nums)
        for i in range(n-1):
            for j in range(i+1,n):
                if (nums[i] + nums[j]) == target:
                    return [i,j]

print(Solution1().twoSum([2,5,5,11],10))

## 2 https://leetcode.com/problems/add-two-numbers/
## test on leetcode | Atempted⭕
from typing import Optional, List

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def traverse(self, n):
        if  n.next:
            return self.traverse(n.next) + str(n.val)
        else:
            return str(n.val)

    def array2ListNode(self,arr):
        if not arr:
            return None

        head = ListNode(arr[0])
        current = head

        for val in arr[1:]:
            current.next = ListNode(val)
            current = current.next

        return head

class Solution2:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]):
        print('\n--- addTwoNumbers ---')
        n1 = int(ListNode().traverse(l1))
        n2 = int(ListNode().traverse(l2))
        print(n1,n2)
        sum1 = n1+n2
        result = [ int(d) for d in str(sum1)[::-1]]
        print(result)
        ln= ListNode().array2ListNode(result)
        t_ln= ListNode().traverse(ln)
        print('✅',ln, t_ln)

l1=ListNode().array2ListNode([2,4,3]); print('ListNode l1 :: ',ListNode().traverse(l1), l1)
l2=ListNode().array2ListNode([5,6,4]); print('ListNode l2 :: ',ListNode().traverse(l2), l2)
print(Solution2().addTwoNumbers(l1, l2))

## https://leetcode.com/problems/median-of-two-sorted-arrays/description/ | 4 (H) ✅
class Solution4:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        print('\n--- findMedianSortedArrays ---')
        n1 = len(nums1)
        n2 = len(nums2)
        arr = nums1 + nums2
        arr.sort()
        n = n1+n2
        mid = n // 2
        if n % 2 == 0:
            median = (arr[mid-1]+arr[mid])/2
            print(arr,'middle-2: ' , arr[mid], arr[mid+1], 'median: ', median)
            return median
        else:
            median = arr[mid]
            print(arr,'middle/median: ',median)
            return float(median)

print(Solution4().findMedianSortedArrays([1,3], [2]))
print(Solution4().findMedianSortedArrays([1,2], [3,4]))

## 6 https://leetcode.com/problems/zigzag-conversion/
"""
Input: s = "PAYP ALIS HIRI NG", numRows = 4
[ PINA LSIG YAHR PI ]
Output: "PINA LSIG YAHR PI"
Explanation:
P     I    N
A   L S  I G
Y A   H R
P     I

P I N
A L S I G
Y A H R
P I

"""
class Solution6:
    def convert(self, s: str, numRows: int) -> str:
        print('\n--- convert :: Zigzag Conversion #6 ---')
        if numRows == 1 or numRows >= len(s):
            return s

        rows = [''] * numRows # [''0, ''1, ''2] >> or <<
        i = 0
        go_r = False
        for c in s:
            if i == 0 or i == numRows-1:
                go_r = not go_r
                print('switching direction...')

            rows[i] += c # concat char
            print(i, c, rows)

            if go_r: i =i+1
            else: i=i-1
        return ''.join(rows)
print(Solution6().convert("PAYPALISHIRING",3))
print(Solution6().convert("PAYPALISHIRING",4))

"""
---Solution6::convert::zigzag---
switching direction...
0 P ['P', '', '', '']
1 A ['P', 'A', '', '']
2 Y ['P', 'A', 'Y', '']
switching direction...
3 P ['P', 'A', 'Y', 'P']
2 A ['P', 'A', 'YA', 'P']
1 L ['P', 'AL', 'YA', 'P']
switching direction...
0 I ['PI', 'AL', 'YA', 'P']
1 S ['PI', 'ALS', 'YA', 'P']
2 H ['PI', 'ALS', 'YAH', 'P']
switching direction...
3 I ['PI', 'ALS', 'YAH', 'PI']
2 R ['PI', 'ALS', 'YAHR', 'PI']
1 I ['PI', 'ALSI', 'YAHR', 'PI']
switching direction...
0 N ['PIN', 'ALSI', 'YAHR', 'PI']
1 G ['PIN', 'ALSIG', 'YAHR', 'PI']
PINALSIGYAHRPI
"""

## 7 https://leetcode.com/problems/reverse-integer/description/ ✅
class Solution7:
    def reverse(self, x: int) -> int:
        print('\n--- reverse integer---')
        if 0 <= x <= pow(2, 31) - 1:
            reversed = str(x)[::-1]
            if int(reversed) > pow(2, 31) - 1:
                return 0
            return int(reversed)

        elif pow(2, 31) * -1 <= x < 0:
            reversed = str(x)[1:][::-1]
            if int(reversed)*-1 < pow(2, 31) * -1:
                return 0
            return int(reversed) * -1

        else:
            return 0

print(Solution7().reverse(2345))
print(Solution7().reverse(-2345))
print(Solution7().reverse(1534236469))
print(Solution7().reverse(-2147483648))

# https://leetcode.com/problems/palindrome-number/ ✅
class Solution9:
    def isPalindrome(self, x: int) -> bool:
        print("\n--- 9::isPalindrome ---")
        if pow(2, 31) * -1 <= x <= pow(2, 31) - 1:
            rev = str(x)[::-1]
            print('num: ',x, 'rev num: ',rev)
            return True if str(x) == rev else False

print(Solution9().isPalindrome(121))
print(Solution9().isPalindrome(-121))