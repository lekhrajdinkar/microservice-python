# https://leetcode.com/problems/substring-with-concatenation-of-all-words/?envType=study-plan-v2&envId=top-interview-150

class Solution30:
    def findSubstring(self, s: str, words):
        from itertools import permutations
        cs = [''.join(p) for p in permutations(words)]
        result = []
        print('concatenated string :: ',cs)

        cslen = 0
        if cs is not None:
            cslen=len(cs[0])

        i=0
        while(i <= len(s)-cslen):
            _s = i
            _e = i+cslen
            subsstr = s[_s:_e]
            print(f'comparing substr : {subsstr} ({_s}-{_e}) with {cs}')
            if subsstr in cs:
                result.append(i)
                print(f"found✅ at {i}")
                i+=1
            else:
                i+=1

        return result

#print(Solution30().findSubstring("barfoothefoobarman", ["foo","bar"]))
#print(Solution30().findSubstring("ffffffffffffffffffffffff", ["a","a","a","a"]))

"""
concatenated string ::  ['foobar', 'barfoo']
comparing substr : barfoo (0-6) with ['foobar', 'barfoo']
found✅ at 0
comparing substr : thefoo (6-12) with ['foobar', 'barfoo']
comparing substr : hefoob (7-13) with ['foobar', 'barfoo']
comparing substr : efooba (8-14) with ['foobar', 'barfoo']
comparing substr : foobar (9-15) with ['foobar', 'barfoo']
found✅ at 9
[0, 9]
"""

# 209 Minimum Size Subarray Sum (M)
# https://leetcode.com/problems/minimum-size-subarray-sum/?envType=study-plan-v2&envId=top-interview-150
class Solution209:
    def minSubArrayLen(self, target: int, nums) -> int:
        n = len(nums)
        result = []
        for i in range(n):
            sum = 0
            for j in range(i,n):
                sum += nums[j]
                if target <= sum:
                    print(f'index {i}', nums[i:j+1], f'sum ({target}++) :: ',sum, 'length::', j-i+1)
                    result.append(j-i+1)
        return min(result)

print('209 :: ',Solution209().minSubArrayLen(7, [2,3,1,2,4,3]))