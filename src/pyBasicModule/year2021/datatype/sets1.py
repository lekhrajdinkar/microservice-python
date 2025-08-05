# sets are un order. keys in dictionary are ordered
# set is imp mathematical concept
# operation : membership test/in, UNION/U, difference/D, intersection/I, symetric difference / SD = (U-I),
# operator : < > = !
# superset and subset
# set is not sequence, not indexing.
# set uses hash to stor values, hence item must be hashable. (immutable are hashable)

# A. Create
d = {'k1': 1, 'k2':2}; s1 = set(dict.fromkeys(d)); print(s1)
d = {1:1, 2:2}; s1 = set(dict.fromkeys(d)); print(s1)
print(set(range(10)))
s1 = {'app1', 'app3', 'app2', 32}
s2 = {'app1', 'app2', 'app3', 'app3', 32} # like dict but without value part
print(s1) # notice order are diff : {'app2', 'app1', 'app3'}
# print(s1[0])  # TypeError: 'set' object is not subscriptable
# s1 = { ['app1'], ['app2']}; print(s1) #TypeError: unhashable type: 'list'
print( s1 == s2) # t


# B. operations : Add, remove
s1.add('cars'); print(s1) # not append
s1.remove('app1');print(s1); # s1.remove('app1-1');print(s1)
s1.discard('app1-1') ;print(s1) # no error if app1-1 does not exist
s1.pop() ;print(s1.pop()) # randomly remove any item an return item too, diff behv from dict.

even = set(range(0,10,2)); odd = set(range(1,10,2)); even1 = set(range(0,8,2));
s=even | odd ; print(even, odd, s) #union
s=even.union(odd) ; print(even, odd, s)

# B. operators - | - ^ &
s1 = {'A', 'B', 'C', 'D'} ; print(s1)
s2 = {'A', 'B', 'C', 'D', 'E', 'F'} ;print(s2)
s3 = { 'E', 'F', 'G'} ;print(s3)

s = s1 ^ s2 ; print('sym diff : ', s);  # s1 ^= s2 ; print('sym diff : ', s1)
s = s1 | s2 ; print('union : ',  s);  # s1 |= s2 ; print(' update: ',  s1)
s = s2 - s1 ; print('difference : ',  s) ; # s2 -= s1 ; print('difference : ',  s1)
s = s1 & s2 ; print('intersection : ',  s);  # s1 &= s2 ; print('intersection : ',  s1)

# Methods have adv over operator
# methods - union, intersection, difference, symetric_difference
# methods - update, intersection_update, difference_update, symetric_difference_update
print(id(s1), s1 );  s1_new = s1.union(s3); print(id(s1_new), s1_new)  # creates new set
print(id(s1), s1 );  s1.update(s2); print(id(s1), s1) # updates S1, union_update

s1.update('X'); print(s1) # Also pass individual item
s1.update('X','Y','Z'); print(s1) # Also pass individual item
l = ['XX','YY','ZZ']; print(*l) #unpack sequence
s1.update(l); print(s1) # Also pass individual item




# Exercise
while True:
    choice = input('enter choice : 1.add 2.delete 3.update rest.exit : ')
    if choice in '123': # should nt work for 12 and 23
        if choice in set('123'): # list('123') is ok too, but set is faster since it use hashing, even if list in in millions.
        # if choice in {'1', '2', '3'} how we create set also matter, this is more fast.
            print('ur choice : ', choice)
    else:
        break

# Exerceisd : empty set using lterals
s = {} # dict
s = {*""} # set
s = {*{}}
s = set()
s.add('32'); s.add(32); print(s)

# Exerceis  : use case of superset and subset
skills_for_job = {'python', 'ng'}
candidates = {
    'manisha' : {'altyrex', 'excel', 'ng'},
    'lek': {'java', 'python', 'ng'}
}

for candidate, skill_set in candidates.items():
    #if skill_set.issuperset(skills_for_job):
    if skill_set > skills_for_job :
        print(candidate, 'is eligible for interview')

