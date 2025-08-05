## Leet code :: 27 ✅
## https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/?envType=study-plan-v2&envId=top-interview-150
class Solution:
    def removeElement(self,nums, val):
        result = list(filter(lambda x: x != val, nums))
        print(result)
        nums[:] = result
        return len(nums)

print(Solution().removeElement([3,2,2,3],3))
print(Solution().removeElement([0,1,2,2,3,0,4,2],2))