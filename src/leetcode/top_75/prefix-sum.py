# https://leetcode.com/problems/find-the-highest-altitude/?envType=study-plan-v2&envId=leetcode-75 ✅ (E)
class Solution1732:
    def largestAltitude(self, gain) -> int:
        start=0
        result = [0]
        for g in gain:
            net_gain = g+start
            print(f'{g:>3} + {start:>3} = {net_gain:>3}')
            result.append(net_gain)
            start=net_gain

        print(result)
        return max(result)

print(Solution1732().largestAltitude([-5,1,5,0,-7]))
print(Solution1732().largestAltitude([-4,-3,-2,-1,4,3,2]))

print("========================")

## https://leetcode.com/problems/find-pivot-index/?envType=study-plan-v2&envId=leetcode-75
class Solution724:
    def pivotIndex(self, nums) -> int:
        print('✔️',nums)
        n = len(nums); sum1=0
        prefix_sum = []
        for i in range(n):
            sum1 += nums[i]
            #prefix_sum.append(sum(nums[:i+1]))
            prefix_sum.append(sum1)
        print('📚prefix_sum :: ', prefix_sum)

        for i in range(n):
            sum_l = sum(nums[:i]);
            sum_r = sum(nums[i+1:])
            print(f'🔸index {i} :: L {nums[:i]} {sum_l} :: R {nums[i+1:]} {sum_r}')

            sum_l = 0 if i == 0 else prefix_sum[i-1]
            sum_r = prefix_sum[n-1] - prefix_sum[i]
            print(f'  index {i} :: L {nums[:i]} {sum_l} :: R {nums[i+1:]} {sum_r}')

            if sum_l == sum_r:
                return i

        return -1

print('724 :: ',Solution724().pivotIndex([1,7,3,6,5,6]))
print('724 :: ', Solution724().pivotIndex([1, 2, 3]))
print('724 :: ', Solution724().pivotIndex([2, 1, -1]))