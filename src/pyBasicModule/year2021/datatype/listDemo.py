friends = ["liu", "Anna", "dinkar", "lekhraj"]
friends.sort(); print(friends)

print(id(friends[0])) ; print(id(friends))
print(friends[::-1]) #reverse
print(friends[0:3]) ; print(friends[:3]) # first three
print(friends[-3:]) # last three

friends += ["Dr ko"] #addiotion to list
friends.append("Dr Ok")
print(friends);
print(id(friends[0])) ; print(id(friends))

# immutable :  str int float tuple byte frozenset
# mutable: list, set, dict, byteArray

print( 'More operators on seq', '-' * 50)
print(len(friends))
print(friends.count("liu"))

print( '\nMore operators on seq', '-' * 50)
l = [1,2,3,4,5,6,7]
print(min(l)) ; print(max(l)); l.append(8); print(l) #None ? append returns None

l = ["abc", "xyz"]
print(min(l)) ; print(max(l)); print(l.append("ijk"))
l.append("ijk"); print(l); print(l.index('ijk'))
l.remove("abc"); print(l)
j= l.copy(); print(id(l)); print(id(j))



print( '\nwithout Enumerate fn', '-' * 50)
for item in friends:
    print(" {} : {}".format(friends.index(item)+1, item))
print( 'with Enumerate fn', '-' * 50)
for i, item in enumerate(friends):
    print(" {} : {}".format(i+1, item))



print( '\nwithout Enumerate fn', '-' * 50)
temp = [i for i, item in enumerate(friends)] ; print(temp)
temp = [item for i, item in enumerate(friends)] ; print(temp)
temp = [str(i) + f" : {item}" for i, item in enumerate(friends)] ; print(temp)


print( '\nSorting', '-' * 50)
even = [2,4,6,8,10] ; odd =[1,3,5,7,9]
even.extend(odd);
even.sort(reverse=False); print(even) #dafult #sort return same obkect, mutable
even.sort(reverse=True); print(even)

friends = "Liu Anna dinkar Lekhraj";
new_frined = sorted(friends) ; print('new_frined', new_frined) # return new seq/list, sort returns none
# thats the diff between sort method and sorted function
print(friends) # hence original list remain unsorted
#friends.sort(); print(friends)  # sort does not work on str, it works on list
fl = list(friends); fl.sort(key=str.casefold) ; print(fl, "\n",list(friends))


print( '\nPython Build in Function', '-' * 50)
print('SUM :',sum(even))
print("bin : ",bin(even[0]))
print("bool: ",id(even), '| ', id(bool(even)))

print( '\ndelete', '-' * 50)
l1=["abc", "xyz", 'ijk']
l2="abcxyzijk"
l3=[1,2,3,4,5]

del l1[:1] ; print(l1);
#del l2[3:7];print(l2[3:7]); #'str' object does not support item deletion
l22 = list(l2); del l22[3:7]; print(l22)

print( '\nDelete and keep number between 5 to 10 in list', '=' * 50)
min = 5; max = 10;
numbers=[100, 2,4, 50, 76,98, 1, 6, 7, 8, 90, 10, 0,99];
numbers.sort(); print(numbers)
#del numbers[numbers.index(max):] ; del numbers[:numbers.index(min)]; print(numbers)
#del numbers[9:] ; del numbers[:4]; print(numbers);
stop = 0
for index, num in enumerate(numbers):
    if num >= min:
        start = index; print(start); break
print('deleting : ', numbers[:start])
del numbers[:start]
print(' result half : ',  numbers)

for index, num in enumerate(numbers):
    if num >= max:
        end = index+1; print(end); break
print('deleting : ', numbers[end:])
del numbers[end:]
print('result full: ',numbers)

print(  '=' * 50)
# shorter deleting from backwards without sorting
numbers=[100, 2,4, 50, 76,98, 1, 6, 7, 8, 90, 10, 0,99];
for i in range(len(numbers)-1, -1, -1):
    print('\n',i, numbers)
    if numbers[i] > max or numbers[i] < min:
        print('FALSE : ', min,'<=', numbers[i], '<=', max)
        del numbers[i]
    else:
        print('TRUE : ', min, '<=', numbers[i], '<=', max)
print('Final result : ',numbers)

print( 'Better way ro iterate in reverse order', '=' * 50)
numbers=[100, 2,4, 50, 76,98, 1, 6, 7, 8, 90, 10, 0,99];
top_index = len(numbers) - 1;
for index, num in enumerate(reversed(numbers)):
    print(top_index - index, num)


print( '\nstr to list and vice versa', '=' * 50)
print(list("lekhraj Dinkar"))
print([l for l in "lekhraj Diknar"])

# lsit to str
l = ['l', 'e', 'k', 'h', 'r', 'a', 'j', ' ', 'D', 'i', 'n', 'k', 'n', 'a', 'r']
s=''
for i in l:
    s += i
print(s)

print( '\nCopy list', '-' * 50)
l_copy = l.copy() ; print(l_copy)
l_copy = l[:]; print(l_copy)
l_copy = list(l); print(l_copy)

my_digits = [1, 2, 3, 4, 5, 6, 7, 8, 9, ]
my_digits_unsorted = [2, 3, 4, 5, 6, 7, 8, 9, 1 ]
digits = "123456789"
nums = [int(d) for d in digits]; print(nums)
nums_more = nums.copy();
print(id(nums), id(nums_more), nums is nums_more) # false
print(nums == nums_more) # t
print(nums == my_digits) #true
print(nums == my_digits_unsorted) #false

nums_ref = nums; print(id(nums), id(nums_ref), nums is nums_ref)

print( '\nCopy list', '-' * 50)
l = ["app1", "app2", "app3"]
l[2] = "C-star"; print(l)
l[:2] = ["ACS"]; print(l);
l[:] = ["ACS"]; print(l)

print( '\nrange with negative steps', '-' * 50)
l =[1,2,3,4,5]
for i in range(1,len(l)+1,-1): print(i)
for i in range(len(l),-1,-2): print(i)






