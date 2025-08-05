import print_color

def sum(a,b,c):
    print('SUM: ',a+b+c)

sum(10,20,30); sum('a','b','c');

# lets use tuple or any sequence type
t = (10,20,30); sum(*t) # Pack tuple while function calling
sum(*"lek")
sum(*['l','e','k'])
sum(*('l','e','k'))
sum(*(['l', 'e'] ,['k','h'], ['r', 'a', 'j']))
sum(*(['l', 'e'] ,['k','h'], ['r', ['a', 'j']]))
print('+' * 50)
# what if we have add 4 numbers, create new sum function ith 4 agrs. see better way

args = (10,20,30,40,50,60);
args2 = (10,20,30,40,50,60,70);

# variable argument length function
def sum2(*t): #  function defination Un-Packs tuple
    temp = ''
    print(t)
    for n in t:
        temp +=str(n)
    agrs = 'CONCAT:', temp
    print(agrs)
    print_color.myprint(print_color.GREEN, *agrs) # keep packing of tuple args here
    print_color.myprint(print_color.UNDERLINE, 'CONCAT:', temp); #IMP
    print_color.myPrintWithMoreEffect(('CONCAT:' + temp), print_color.UNDERLINE, print_color.GREEN)
    print_color.myPrintWithMoreEffect2(print_color.UNDERLINE, print_color.GREEN, text=('CONCAT:' + temp))
    print();

sum2(*args)
sum2(*args2)
sum2(*"lekhu")
sum2(*['l','e','k','h','u'])

def paramterTypeExplained(p, *args, k0, **kvargs):
    print('postional-or-keyword......', p)
    print('var-positional(args)......', args)
    print('keyword...................', k0)
    print('var-keyword...............', kvargs)
paramterTypeExplained('pos', 1,2,3,4,5, k0='value0', k1='k1',k2="key2")


