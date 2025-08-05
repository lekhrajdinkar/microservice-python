class Solution189:
    def rotate(self, nums, k: int) -> None:
        # k can be more than length of nums
        k = k % len(nums)
        # [12345] k=4 | [123][45] | [45][123]
        nums[:] = nums[-k::] + nums[:-k:]
        print(nums)
print(Solution189().rotate([1,2,3,4,5], 3))

class Solution191:
    def hammingWeight(self, n: int) -> int:
        b = bin(n)[2:]
        print(n,b)
        return str(b).count('1')

print(Solution191().hammingWeight(123))


# 14 https://leetcode.com/problems/longest-common-prefix/description/?envType=study-plan-v2&envId=top-interview-150
class Solution14:
    def longestCommonPrefix(self, strs) -> str:
        result = ''
        n = len(strs)
        for chars in zip(*strs):
            print(chars, chars[0])
            if chars.count(chars[0]) == n:
                result += chars[0]
            else:
                break
        print(result)
        return result

Solution14().longestCommonPrefix(["flower","flow","flight"])

# 392 https://leetcode.com/problems/is-subsequence/?envType=study-plan-v2&envId=top-interview-150
class Solution392:
    def isSubsequence(self, s: str, t: str) -> bool:
        #index = -1
        result = True
        for i in s:
            print(f'\nlooking "{i}" inside parent string "{t}"')
            if t.find(i) != -1:
                index = t.find(i)
                t = t[(index+1):]
                print(f'found {i} at index {index}, updating index to: {index} | new parent string {t}')
            else:
                result = False
                break

        return result

#print(Solution392().isSubsequence("abc", "ahbgdc"))
print(Solution392().isSubsequence("twn", "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxtxxxxxxxxxxxxxxxxxxxxwxxxxxxxxxxxxxxxxxxxxxxxxxn"))


