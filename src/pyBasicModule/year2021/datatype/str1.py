name="Hello Liu!! 'How are You'"

def string_demo():
    # prg-1
    print('original string ', name)
    print('slice 1 ',name[:6])
    print('slice 2 ',name[6:] )
    print('slice 3, step -1',name[::-1]) # reverse string
    print('slice 3, step -2',name[::-2])
    print('slice 4, step 2',name[::1])
    print(name)

    # prg-2
    n="0123456789" ;
    print('⛔number String: ', n)
    print('⛔indexing',n[9] , n[-1], n[9-10], n[-6:-1:2]) # positive index - lenght : 3rg: Step

    # prg-3 : print seperator
    n="_1234+1234_1234?1234" ; print(n[0:n.__sizeof__():5])
    seperator = n[0::5] ; print(seperator)
    for i in n: # prepare seperator way 2
        if not i.isnumeric(): # ⬅️
            seperator = seperator + i
    value = "".join(char if char not in seperator else " " for char in n).split()

    # prg-4: see ways to print
    print(int(v) for v in value) #generator object <genexpr> at 0x7f8e1ee82890
    print([int(v) for v in value])
    for v in value:
        print(v)

    # prg-5 : backslicing / negative steps
    letter='abcdefghijklmnopqrstuvwxyz';
    print('back Slicing', letter[25:-1:-1], " | ", letter[25:25:-1]); #same, using negative indexing
    print('back Slicing', letter[25:-2:-1], " | ", letter[25:24:-1]); #same, using negative indexing
    print('back Slicing', letter[25::-1]); #end in 0, if negative step
    print('back Slicing', letter[::-1]); #end in 0, if negative step n start is max index
    print('back Slicing challenge : last 8 : ', letter[25:-9:-1])
    print('back Slicing challenge : qpo: ', letter[-10:-13:-1], ' ,edbca:' , letter[4::-1])

    # triple quotes
    text="""
    Hello Liu!! 
    what are u doing 
    'How are You'  
    """;
    print(text)

    # escape
    print("Pet clinic by \"Spring boot\" ")
    print('Pet clinic by "Spring boot"')
    print(r"C:\Users\tim\nice")
    print("C:\\Users\\tim\\nice")

    # String function... check doc
    print("aBc".capitalize())
    print("aBc".swapcase())
    print("aBc".casefold())
    print("ABC".isupper())









