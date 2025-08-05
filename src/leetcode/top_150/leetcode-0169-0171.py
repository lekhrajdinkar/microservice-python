# https://leetcode.com/problems/majority-element/?envType=study-plan-v2&envId=top-interview-150
# 169. Majority Element ✅
class Solution:
    def majorityElement(self, nums) -> int:
        #n = len(nums)//2
        n = (len(nums)+1)//2
        print('n/2', n)
        for i in set(nums):
            if nums.count(i) >= n:
                return i

        return 0

print(Solution().majorityElement([3,2,3]))  # Output: 3
print(Solution().majorityElement([2, 2, 1, 1, 1, 2, 2]))  # Output: 2


# https://leetcode.com/problems/excel-sheet-column-number/
# 171. Excel Sheet Column Number ✅
print(171,"-"*50)
class Solution:
    # ❌
    def titleToNumber2(self, columnTitle: str) -> int:
        n = len(columnTitle)

        total_sum = 0
        for i in range(n):
            pos = (n-1)-i # index from back
            c = columnTitle[pos:pos+1]
            p = pow(total_sum,i)
            code = (ord(columnTitle[pos]) - 64)
            sum = p + code
            total_sum  += sum
            print(f"char {c} at {i} | code: {code} | 26^{i}: {p} | sum : {sum} | total_sum : {total_sum}")

        return total_sum

    # ✅
    def titleToNumber(self, columnTitle):
        result = 0
        for char in columnTitle:
            print('before', result)
            result = result * 26 + (ord(char) - 64)
            print('after', result)

        return result

print(Solution().titleToNumber("BA"))



