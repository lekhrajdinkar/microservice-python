## Leet code :: 26 ✅
## https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/?envType=study-plan-v2&envId=top-interview-150
class Solution:
    def removeDuplicates(self, nums) -> int:
        nums[:] = list(set(nums))
        nums.sort()
        return len(nums)

print(Solution().removeDuplicates([1,1,2]))  # Output: 2


# Leet code :: 80 ✅
# https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/description/?envType=study-plan-v2&envId=top-interview-150
# ✔️ each unique element appears at most twice.
class Solution80:
    def removeDuplicates(self, nums) -> int:
        #nums.sort()
        counter_dict = {}
        for i in set(nums):
            counter_dict[i] = nums.count(i)

        for key, value in counter_dict.items():
            if value > 2:
                for i in range(value - 2):
                    nums.remove(key)

        return len(nums)

print(Solution80().removeDuplicates([1,1,1,2,2,3]))  # Output: 5
print(Solution80().removeDuplicates([0, 0, 1, 1, 1, 1, 2, 3, 3]))  # Output: 7
print(Solution80().removeDuplicates([1, 1, 1, 2, 2, 3]))  # Output: 5