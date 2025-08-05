# 172 : https://leetcode.com/problems/factorial-trailing-zeroes/description/

class Solution:
    def trailingZeroes(self, n: int) -> int:
        def fact(n1):
            if n1 == 0:
                return 1
            return n1 * fact(n1-1)

        f = fact(n)
        print(f'factorial is {str(f)}:')

        import sys
        #sys.set_int_max_str_digits(10000)
        zero_count = 0
        l =  [int(d) for d in str(f)]
        n = len(l)
        for i in range(n-1, -1, -1):
            if int(l[i]) == 0:
                zero_count +=1
            else:
                break

        return zero_count

print(Solution().trailingZeroes(7))      # Output: 1