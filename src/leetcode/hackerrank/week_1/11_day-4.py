## =========== 1. character grid ==========
"""
a b c
a d e
e f g

col-1 : a a e sorted
col-2 : b d f sorted
col-3 : c e g sorted
"""

def gridChallenge(grid):
    un_sorted_grid = [list(row) for row in grid]
    sorted_grid = [sorted(row) for row in grid]
    print('un-sorted-grid',un_sorted_grid)
    print('sorted-grid',sorted_grid)

    for cols in zip(*sorted_grid):
            if list(cols) != sorted(cols):
                print ("Not Sorted (col-wise)", list(cols), sorted(cols))
                return "NO"
            else:
                print ("Sorted (col-wise)", list(cols), sorted(cols))
    return "YES"

grid1 = ['abc','ade', 'efg']
grid2 = ['abc','ade', 'gfa']
grid3=['eabcd','fghij','olkmn','trpqs','xywuv']
print(gridChallenge(grid2))


print("# ========  2. Super digit ==========================")
"""
super_digit(9875)   	9+8+7+5 = 29 
	super_digit(29) 	2 + 9 = 11
	super_digit(11)		1 + 1 = 2
	super_digit(2)		= 2 
"""
def superDigit(n):
    print("n", n)
    if len(n) == 1:
        print("len(n)", len(n))
        return int(n)
    else:
        sum = 0
        for i in n:
            #print(f'next digit in number {n} : ', i)
            sum += int(i)
        #sum = sum * k
        print("super digit ", sum)
        return superDigit(str(sum))

result = superDigit('148')
print('result',result)

print("# ========  3. too Chaotic ==========================")

def minimumBribes(q):
    b_count = 0
    for i in range(len(q)):
        if q[i] - (i + 1) > 2:
            print("Too chaotic")
            return
        for j in range(max(0, q[i] - 2), i):
            if q[j] > q[i]:
                b_count += 1
    print(b_count)


minimumBribes([1,2,3,4])
minimumBribes([2,1,3,4])
minimumBribes([2,1,4,3])
minimumBribes([4,2,1,3])
