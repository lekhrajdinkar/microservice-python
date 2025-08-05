from typing import List
class Solution:
    # 🫱🏻 1071 https://leetcode.com/problems/greatest-common-divisor-of-strings/?envType=study-plan-v2&envId=leetcode-75
    def kidsWithCandies(self, candies: List[int], extraCandies: int) -> List[bool]:
        print("\n1071---kidsWithCandies---")
        candies_max = [ i + extraCandies for i in candies]
        print(candies_max)
        n = len(candies)
        result=[]
        for i in range(n):
            if candies_max[i] >= max(candies):
                result.append(True)
            else:
                result.append(False)
        return result

    # 345 🫱🏻 https://leetcode.com/problems/reverse-vowels-of-a-string/description/?envType=study-plan-v2&envId=leetcode-75
    def reverseVowels(self, s: str) -> str:
        print("\n345---reverseVowels---",s)
        vowels = ['a','e','i','o','u','A','E','I','O','U']
        words=list(s)
        n=len(s)
        l=0
        r=n-1
        while l < r:
            if words[l] in vowels and words[r] in vowels:
                words[l], words[r] = words[r], words[l] # swap
                print('🔸swapping',l,r,words)
                l+=1
                r-=1
                print('moving l and r ',l,r,words)
            elif words[l] not in vowels and words[r] not in vowels:
                l+=1
                r-=1
                print('moving l and r ',l,r,words)
            elif words[l] not in vowels and words[r] in vowels:
                l+=1
                print('moving l++',l,r,words)
            elif words[l] in vowels and words[r] not in vowels:
                r-=1
                print('moving r--',l,r,words)

        result= ''.join(words)
        return result

    # 605 🫱🏻 https://leetcode.com/problems/can-place-flowers/?envType=study-plan-v2&envId=leetcode-75
    ## wasted time so cheated ⭕⭕
    def canPlaceFlowers(self, flowerbed: List[int], n: int) -> bool:
        if n == 0:
            return True
        for i in range(len(flowerbed)):
            if flowerbed[i] == 0 and (i == 0 or flowerbed[i-1] == 0) and (i == len(flowerbed)-1 or flowerbed[i+1] == 0):
                flowerbed[i] = 1
                n -= 1
                if n == 0:
                    return True
        return False

# ========== RUN ==========

print(Solution().kidsWithCandies([2,3,5,1,3],3))
print(Solution().kidsWithCandies([4, 2, 1, 1, 2], 1))
print(Solution().kidsWithCandies([12, 1, 12], 10))

print(Solution().reverseVowels("IceCreAm"))
print(Solution().reverseVowels("leetcode"))

print(Solution().canPlaceFlowers([1,0,0,0,1],1))
print(Solution().canPlaceFlowers([1, 0, 0, 0, 1], 2))
print(Solution().canPlaceFlowers([1, 0, 0, 0, 0, 1], 2))
print(Solution().canPlaceFlowers([1, 0, 0, 0, 0, 0, 1], 2))
