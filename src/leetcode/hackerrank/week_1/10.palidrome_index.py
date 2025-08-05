def palindromeIndex(s):
    n = len(s)
    if s == s[::-1]:
        return -1
    for i in range(n//2):
        s1 = s[(i+1):] # Try removing left character
        s2 = s[:(n-1-i)] # Try removing right character
        if(s1 == s1[::-1]):
            print('remove left', s1, ',its reverse matching ', s1[::-1])
            return i
        elif (s2 == s2[::-1]):
            print('remove right', s2, ',its reverse matching ', s2[::-1])
            return (n-1-i)
        else:
            print('both not worked ', i, s1, s2)

    return -1


s = 'eeecbcbcb'
result = palindromeIndex(s)
print(s, result)