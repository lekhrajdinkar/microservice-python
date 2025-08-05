# 283 https://leetcode.com/problems/move-zeroes/?envType=study-plan-v2&envId=leetcode-75
## Sliding Window
class Solution283:
    def moveZeroes(self, nums) -> None:
        print('Before ',nums)
        nums[:] = list(filter(lambda x: x!= 0, nums)) + ([0]*nums.count(0))
        print('After ',nums)
        return nums

print('283 :: ',Solution283().moveZeroes([0,1,0,3,12]))

# 1679 https://leetcode.com/problems/max-number-of-k-sum-pairs/?envType=study-plan-v2&envId=leetcode-75
print('-'*10,   'Solution1679', '-'*10  )
class Solution1679:
    # ❌
    def maxOperations_1(self, nums, k: int) -> int:
        #nums.sort()
        n = len(nums)
        result = 0; l = 0; l2 = 1
        while nums:
            sum=nums[l] + nums[l2]
            print(f'{nums[l]}({l}) + {nums[l2]}({l2}) = {sum}',  ' | ', nums)
            if sum == k:
                result += 1
                del nums[l];  del nums[l2-1]
                print('❌post del', nums)
                l = 0; l2 = 1;  n = n-2
            else:
                if l2 < n-1:
                    l2 += 1;  print(f'--increment l2, n:{n} --', l2)
                elif l < l2-1:
                    l += 1;    print(f'--increment l1:{l}, n:{n}, l2:{l2} --')
                else:
                    print(f'--reached max :: l1:{l}, n:{n}, l2:{l2} --')
                    break

        #print(f'maxOperations :: result {result}')
        return result

    # ✅
    def maxOperations(self, nums, k: int) -> int:
        count = 0; n = len(nums)
        l = 0; r = n -1
        nums.sort()
        while(l<r):
            sum = nums[l] + nums[r]
            if sum == k:
                count += 1
                l += 1; r -= 1
            elif sum < k:
                l += 1
            else:
                r -= 1

        return count

print('1697_1',Solution1679().maxOperations_1([1,2,3,4],4)) # ❌
print('1697_1',Solution1679().maxOperations_1([3,1,3,4,3],4)) # ✅

print('1697_2',Solution1679().maxOperations([1,2,3,4],4))
print('1697_2',Solution1679().maxOperations([3,1,3,4,3],4))