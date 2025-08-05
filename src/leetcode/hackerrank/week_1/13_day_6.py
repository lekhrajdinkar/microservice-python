## ligo Block
# ❌ will do later

## https://www.hackerrank.com/challenges/one-week-preparation-kit-jesse-and-cookies/problem
## jesse-and-cookies ✅
def cookies(k, A):
    A.sort()
    result = 0
    mix = len(A)>=2 and len(list(filter(lambda x: x<k, A))) > 0
    c=0
    print (f'Now A = {A}')
    while (mix and c < len(A)-1):
        if A[c] < k:
            t= A[c] + (2*A[c+1])
            print (f'\nRemove {A[c]} {A[c+1]} and return  {A[c]} + ({A[c+1]} * 2) = {t}')
            del A[0:2]
            A.insert(c,t)
            A.sort()
            print (f'Now A = {A}')
            result += 1

        else:
            c += 1

        mix = len(A)>=2 and len(list(filter(lambda x: x<k, A))) > 0

    return result

#cookies(7, [1,2,3,9,10,12])
print(cookies(9, [2,7,3,6,4,6]))

"""
Now A = [2, 3, 4, 6, 6, 7]

Remove 2 3 and return  2 + (3 * 2) = 8
Now A = [4, 6, 6, 7, 8]

Remove 4 6 and return  4 + (6 * 2) = 16
Now A = [6, 7, 8, 16]

Remove 6 7 and return  6 + (7 * 2) = 20
Now A = [8, 16, 20]

Remove 8 16 and return  8 + (16 * 2) = 40
Now A = [20, 40]
4
"""

# Complete the 'fizzBuzz' function below.
# The function accepts INTEGER n as parameter.
def fizzBuzz(n):
    for i in range(1,n+1):
        if i%3==0 and i%5==0:
            print('FizzBuzz')
        elif i%3==0:
            print('Fizz')
        elif i%5==0:
            print('Buzz')
        else:
            print(i)