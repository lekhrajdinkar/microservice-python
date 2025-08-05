from collections import Counter
from typing import List

class Solution:
    ## ✅ 1207 https://leetcode.com/problems/unique-number-of-occurrences/?envType=study-plan-v2&envId=leetcode-75
    def uniqueOccurrences(self, arr: List[int]) -> bool:
        print('--- uniqueOccurrences ---', arr)
        r = {}
        set1 = set(arr)
        for i in set1:
            count = arr.count(i)
            print(i, r)
            if count in r.keys():
                print(count, 'found again ...')
                return False
            else:
                r[count] = i

        return True

    ## ✅ 2215 https://leetcode.com/problems/find-the-difference-of-two-arrays/submissions/1704172351/?envType=study-plan-v2&envId=leetcode-75
    def findDifference(self, nums1: List[int], nums2: List[int]) -> List[List[int]]:
        print("\n---- findDifference ---")
        answer = [ set(), set() ]
        print(answer)

        for i in nums1:
            if i not in nums2:
                answer[0].add(i)
        print(answer)

        for i in nums2:
            if i not in nums1:
                answer[1].add(i)
        print(answer)

        return [ list(a) for a in answer]

    # 1657. Determine if Two Strings Are Close
    # https://leetcode.com/problems/determine-if-two-strings-are-close/description/?envType=study-plan-v2&envId=leetcode-75
    def closeStrings(self, word1: str, word2: str) -> bool:
        if set(word1)!=set(word2):
            return False
        freq1=Counter(word1)
        freq2=Counter(word2)
        return sorted(freq1.values())==sorted(freq2.values())

    # 2352. Equal Row and Column Pairs ✅
    # https://leetcode.com/problems/equal-row-and-column-pairs/?envType=study-plan-v2&envId=leetcode-75

    def equalPairs(self, grid: List[List[int]]) -> int:
        print("\n 🔸---- equalPairs ---")
        n = len(grid)
        dr = {}
        dc = {}
        count = 0
        for i in range(n):
            print(grid[i])
            dr[i] = '-'.join(str(num) for num in grid[i])
        print(dr)

        for i,t in enumerate(zip(*grid)):
            dc[i] = '-'.join(str(num) for num in t)
            for k in range(n):
                if dc[i] == dr[k]:
                    print(f'r({k}), c({i}) matches == ( {dr[k]} , {dc[i] } )')
                    count +=1
        print(dc)
        return count
    """
     🔸---- equalPairs ---
    [3, 1, 2, 2]
    [1, 4, 4, 5]
    [2, 4, 2, 2]
    [2, 4, 2, 2]
    
    dict row: {0: '3-1-2-2', 1: '1-4-4-5', 2: '2-4-2-2', 3: '2-4-2-2'}
    dict col: {0: '3-1-2-2', 1: '1-4-4-4', 2: '2-4-2-2', 3: '2-5-2-2'}
    
    r(0), c(0) matches == ( 3-1-2-2 , 3-1-2-2 )
    r(2), c(2) matches == ( 2-4-2-2 , 2-4-2-2 )
    r(3), c(2) matches == ( 2-4-2-2 , 2-4-2-2 )
    
    """

# ===========
print('1207', Solution().uniqueOccurrences([1,2,2,1,1,3]))
print('1207', Solution().uniqueOccurrences([1, 2]))
print('1207', Solution().uniqueOccurrences([-3, 0, 1, -3, 1, 1, 1, -3, 10, 0]))

print('✔️2215', Solution().findDifference([1, 2, 3], [2, 4, 6]))
print('✔️2215', Solution().findDifference([1, 2, 3, 3], [1, 1, 2, 2]))

print('✔️2352', Solution().equalPairs([[3, 2, 1], [1, 7, 6], [2, 7, 7]]))
print('✔️2352', Solution().equalPairs([[3, 1, 2, 2], [1, 4, 4, 5], [2, 4, 2, 2], [2, 4, 2, 2]]))
print('✔️2352', Solution().equalPairs([[11,1],[1,11]]))