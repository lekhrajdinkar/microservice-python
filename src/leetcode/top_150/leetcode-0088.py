## Leet code :: 88 ✅ SOLVED ✅
## https://leetcode.com/problems/merge-sorted-array/description/?envType=study-plan-v2&envId=top-interview-150
class Solution(object):
   def merge(self,nums1, m, nums2, n):
                non_zeros = sorted([x for x in nums1 if x != 0], reverse=True)
                zero_count = nums1.count(0)
                nums1_new = non_zeros + [0] * zero_count
                nums1_new[:] = nums1_new[:m]

                print(nums1, nums1_new)
                if len(nums1_new) == 0 and len(nums2) == 0:
                    nums1[:] = []
                elif not nums1_new or len(nums1_new) == 0:
                        nums1[:] = nums2[:n+1]
                elif not nums2 or len(nums2) == 0:
                    nums1[:] = nums1[:m+1]
                else:
                    nums1[:] = nums1_new[:m+1] + nums2[:n+1]

                nums1.sort()
                return nums1


num1=[-1,0,0,3,3,3,0,0,0]
num2=[1,2,2]

print(Solution().merge(num1, 6, num2, 3))