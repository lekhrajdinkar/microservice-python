# 1. if elif else
age = 45 #int(input('enter age'))
if 18 <= age <= 60:
    print('eligible to work in IT')
elif age > 60:
    print(' Senior citizen')
elif age < 18:
    print("kid")

# operators ND OPERATOR PRecedence : check doc.python.doc
# and, or, not, [in , not in]

#try multiple boolean expression
if not '10' in '1000': #try with : 0 f, 0.1 t, -1 t, "" f, "xxxx" t, z' in 'zen':
    print('true block')
else:
    print('false block')

# for loops, can use with iterable type - range(), sequence types, etc
# A. Sequence
for word in ["Anna", "liu"]:
    for char in word:
        print(char)
# B. range
for i in range(1,6):
    print('*' * 5 ,'count {}'.format(i), '*'* 5)

# Exercise  1: print 1 to 9
print([i for i in range(0,10,2)]) #does not include last value
print([i for i in range(10,0,-2)])

# execercise 2: num divisible by 7 between 0 and 100
print([i for i in range(0,101,7)])
print([i for i in range(101)[::7]]) # usinf slicing on sequence, range() would give sequence

