#from src.pyBasicModule.year2021.common_data import data
from ..common_data import data

albums_list = data.albums_list

def demo_tuple_1():
    l = ['ABC', 'DEF', 42] ; print('📃list',l)
    t = ('ABC', 'DEF', 42 ); print('📃tuple',t)
    t = 'ABC', 'DEF', 42 ; print('📃tuple, can omit parenthesis, while assignment ⬅️',t)

    print('⛔regular print', 'ABC', 'DEF', 42 )
    print('⛔print tuple - print((x,x,x))',('ABC', 'DEF', 42 )) # always use parenthesis while using tuple as method argument

    # unpacking
    x,y,z = (10,20,30); print(" ➕unpacked from tuple1 :",x,y,z)
    x,y,z = 10,20,300 ; print(" ➕unpacked from tuple2: ",x,y,z)
    x,y,z= t ; print(" ➕unpacked from tuple3: ",x,y,z)
    x,y,z= "xyz" ; print(" ➕unpack from any sequence 😁, eg:array: ",x,y,z)


    for i, value in enumerate(['a', 'b', 'c']):
        print(i,value, end=', ') # usage of unpacking, enumerate returns tuple.
    for t in enumerate(['a', 'b', 'c']): # ⬅️
        print(t, end=', ')
    for t in enumerate(['a', 'b', 'c']):
        i,v = t
        print(i, v, end=', ')

    print('\n','-'*50)
    t = (('code1', '1234'), ('code2', '2121')) # nested tuple
    for name, (d1, d2, d3, d4) in t: # ⬅️
        print (name, 'unpack part: ', d1,d2,d3,d4)

    # nested indexing ⬅️
    ref = """
    albums_list = [
    ('Eminem', 2000, ['my mom', 'iam not afraid']),
    ('Selena', 2010, ['heart', 'same old love', 'sad']),
    ]
    """
    print('nested indexing: ',albums_list[1][2][2], end='🔚')

    for album  in albums_list :
        artist, year, songs = album
        print ('\n\n',artist, year, songs)
        for song in songs:
            print(song, end='|')

    # list to tuple conversion vice versa ⬅️
    l = ['aa', 'bb','cc']
    t  = (a,b,c) =  l
    print('tuple', t, type(t),  'list: ' , l, type(l))

    l= [a,b,c] = ('aa', 'bb','cc')
    print('list ', l, type(l))



