# ✔️https://www.tryexponent.com/courses/software-engineering/swe-practice/contiguous-subarray-sum-practice
def has_good_subarray(nums, k):
    if nums is None:
        return False
    for i in range (len(nums)-1):
        if (nums[i]+nums[i+1])%k==0:
            return True
    return False

print(has_good_subarray([23, 2, 4, 7], 6))

# ✔️ https://www.tryexponent.com/courses/software-engineering/swe-practice/move-zeros-to-end-of-array-practice
from typing import List

def moveZerosToEnd(arr: List[int]) -> List[int]:
    return list(filter(lambda x: x!=0, arr)) + ([0] * arr.count(0))

print(moveZerosToEnd([0, 1, 0, 3, 12]))

