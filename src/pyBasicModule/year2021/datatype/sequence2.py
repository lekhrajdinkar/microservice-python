from ..common_data import data

menu = data.menu
def loop_seq_1():
    print('way 1 : printing list', '_'*40)
    for meal in menu:
        # print(menu)
        for index in range(len(meal)-1, -1, -1):
            # print(index)
            if meal[index] == 'spam':
                # print('deleting ', menu[index] )
                del meal[index]
        print(meal)

def loop_seq_2():
    print('\nway 2 : end key argument', '_'*40)
    for meal in menu:
        for item in meal:
            if item != 'spam':
                print(item, end=", ")
        print()

def exercise_4():
    items=', '.join(item if item != 'spam' else ''  for meal in menu for item in meal)
    print(items)


def exercise_1():
    paragram="My name is \tAnna Liu, from california, irvine"
    print('-'.join( char    for char in paragram     if not (char == ',' or char == ' ' or char == '\t')).split('-'))
    l = list()
    for char in paragram:
        if char == ',' or char == ' ' or char == '\t': pass
        else: l.append(char)
    print('-'.join(l))

def exercise_2():
    numbers = input('Enter 3 numbers, comma sepaerated')
    numbers=numbers.split(','); print(numbers)
    numbers=[int(n) for n in numbers]; print(numbers)
    a,b,c= numbers; print(a, b, c)
    print(a+b-c)
    print(data.albums_list)








