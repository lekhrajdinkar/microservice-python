## https://leetcode.com/problems/maximum-average-subarray-i/description/?envType=study-plan-v2&envId=leetcode-75
## 643. Maximum Average Subarray I
class Solution643:
    def prefix_sum(self,nums):
        prefix_sum = [0]; sum1 = 0;n = len(nums)
        for i in range(n):
            sum1 += nums[i]
            prefix_sum.append(sum1)
        return prefix_sum

    def findMaxAverage(self, nums, k: int) -> float:
        print("\n---findMaxAverage---")
        avg = -9999999999
        n = len(nums)
        if n == 1:
            return nums[0]
        prefixSum = self.prefix_sum(nums)
        print('prefixSum : ', prefixSum)

        for i in range(n-k+1):
            next_k = nums[i:k+i]
            #sm = sum(next_k)
            sm = prefixSum[k+i] - prefixSum[i]
            new_avg = sm / k
            print(f'next_{k} : {next_k} | sum : {sm} | new avg: {new_avg} | old avg: {avg}')
            if  avg < new_avg :
                print(f"updating to max ... {new_avg}")
                avg = new_avg

        return avg

print('✔️643 ',Solution643().findMaxAverage([1,12,-5,-6,50,3],4))
print('✔️643 ',Solution643().findMaxAverage([5],1))
print('✔️643 ',Solution643().findMaxAverage([0,1,1,3,3],4))
#print('✔️643 ',Solution643().findMaxAverage([493,593,1446,-6013,2163,8450,3008,-1328,6195,4102,-6242,-9971,-8327,4480,-4972,-8305,-1644,2320,331,2465,2955,-8386,-7580,1759,-9576,-8088,-9446,-2916,-3600,923,1412,-5390,4492,9458,-9336,-4754,-3455,9597,-324,-5628,4242,4076,8159,-2423,-3449,6744,9029,-9231,2283,6118,-200,3610,-7566,-6976,2519,9532,2221,-5167,-2370,1861,-1558,-9815,-1186,2021,7050,-4504,4926,8362,7805,-8274,-351,5826,7623,-5520,-2395,-8466,-8461,3261,-3197],7))
#print('✔️643 ',Solution643().findMaxAverage([8860,-853,6534,4477,-4589,8646,-6155,-5577,-1656,-5779,-2619,-8604,-1358,-8009,4983,7063,3104,-1560,4080,2763,5616,-2375,2848,1394,-7173,-5225,-8244,-809,8025,-4072,-4391,-9579,1407,6700,2421,-6685,5481,-1732,-8892,-6645,3077,3287,-4149,8701,-4393,-9070,-1777,2237,-3253,-506,-4931,-7366,-8132,5406,-6300,-275,-1908,67,3569,1433,-7262,-437,8303,4498,-379,3054,-6285,4203,6908,4433,3077,2288,9733,-8067,3007,9725,9669,1362,-2561,-4225,5442,-9006,-429,160,-9234,-4444,3586,-5711,-9506,-79,-4418,-4348,-5891],93))

## https://leetcode.com/problems/maximum-number-of-vowels-in-a-substring-of-given-length/description/?envType=study-plan-v2&envId=leetcode-75
## 1456. Maximum Number of Vowels in a Substring of Given Length
## working but timeout for big array ✔️
class Solution1456_2:
    def isVowel(self,c):
        return  c == 'a' or c == 'e' or c == 'i' or c == 'o' or c == 'u'

    def maxVowels(self, s: str, k: int) -> int:
        #print("\n------- maxVowels -----------")
        vowels = 'aeiou'
        result = 0; n = len(s)
        for i in range(n-k+1):
            curr = s[i:k+i]
            #print(curr)
            count=0
            for c in curr:
                if self.isVowel(c):
                    count +=1
            if count > result:
                result = count
        return result

## Fixing above issue
## not working ❌
class Solution1456:
    def isVowel(self,c):
        return  c == 'a' or c == 'e' or c == 'i' or c == 'o' or c == 'u'

    def countVowels(self, s):
        count = 0
        for c in s:
            if self.isVowel(c):
                count += 1
        return count

    def maxVowels(self, s: str, k: int) -> int:
        print("\n------- maxVowels -----------")
        result = 0
        n = len(s)
        # count vowel for first window then slide by one
        count = self.countVowels(s[:k])
        if count == k: return k

        print( f'count in window of {k}: ({0}-{k-1}) {s[:k]} : count --> 🔸{count}')

        # slide to right by 1
        for i in range(1,n-k):
            if count == k:
                return k
            print(f'slide window to right by 1 ({i}-{i+k}) : {s[i:i+k]}')
            if not self.isVowel(s[i-1]) and self.isVowel(s[i+k-1]):
                count += 1
                print('count --> ➕',count)

            if not self.isVowel(s[i-1]) and not self.isVowel(s[i+k-1]):
                count -= 1
                print('count --> ➖',count)


            if count > result:
                result = count

        return result

print(Solution1456().maxVowels("abciiidef", 3))
print(Solution1456().maxVowels("a", 1))
print(Solution1456().maxVowels("leetcode", 3))


## https://leetcode.com/problems/max-consecutive-ones-iii/description/?envType=study-plan-v2&envId=leetcode-75
## 1004. Max Consecutive Ones III


## https://leetcode.com/problems/longest-subarray-of-1s-after-deleting-one-element/description/?envType=study-plan-v2&envId=leetcode-75
## 1493. Longest Subarray of 1's After Deleting One Element
class Solution:
    def longestSubarray(self, nums) -> int:
        l = 0
        r = 1

## 1233
class Solution1233:
    def removeSubfolders(self, folders):
        print("\n---- removeSubfolders---")
        n = len(folders)
        folders.sort()
        i=0; j=1
        curr = folders[0]
        while True:
            print(folders)
            curr = folders[i]
            while True:
                if curr in folders[j]:
                    del folders[j]
                    # no need to increment j. since del shift to next item
                else:
                    i +=1
                    curr = folders[i]
                    n = len(folders)
                    break
            if i < n-1:
                break

        print(folders)

Solution1233().removeSubfolders(["/a","/a/b","/c/d","/c/d/e","/c/f"])

"""
for f in folders:
            c=f.count('/')
            if level.get(c) is None:
                level[c] = []
            level[c] = level[c] + [f]
        print(level)
"""

## https://leetcode.com/problems/longest-palindromic-substring/description/
class Solution4:
    def longestPalindrome(self, s: str) -> str:
        print("--- longestPalindrome ---")
        t = {}
        n = len(s)
        for  i in range(n):
            for j in range(i,n):
                substr = s[i:j+1]
                if substr==substr[::-1]:
                    t[substr] = len(substr)
        print(t)
        return max(t.keys(), key=t.get)
print(Solution4().longestPalindrome("babad"))