import __main__

a,b=2,4;  c=a+b #  + is def __add__

class Fund:
    category = 'AM'
    self = None # treated as class Attribute
    # 1. new create instance
    # def __new__(cls, *args, **kwargs): pass

    # 2. init just customze instance
    def __init__(self, name, number, share=10):
        pass

    # 3. like java, cannot ommit self keyword, no shorthand

    def __init__(self, name, number, share=10):
        #self = None # 4. It will set instance to None
        self.name = name
        self.number = number
        self.active=False
        self.share=share
        # self.new
        print('&&&&&&&&&&&& COndtructor :: ' , self)
        # 3. return self - cannot return from __init

    # order matte, second occurance will override above defination
    # def __init__(self, name, number, share=10):
    #     pass

    def shareee(self):
        return self.share * 10

    def marketValue(self, price):
        return self.share * price

# update class attribute
Fund.category = 'American Fund'

tdf10 = Fund("TDF10", 11000061, share=20)
tdf10.category ='AFIS' # add attribute same as class attribute
Fund.category = 'American Fund again'
print(tdf10.name, tdf10.number,  tdf10.category, Fund.category,  tdf10.share,type(tdf10) ) #, tdf10.new)
print('share : ', tdf10.shareee())
print('mkt : ', tdf10.marketValue(10))

tdf20 = Fund('TDF20', 11000062); tdf20.share = 50;
print(tdf20.name, tdf20.number, tdf20.category, tdf20.share, type(tdf20))
print()
print('str format 1: {0}'.format(tdf20))
print('str format 2: {0.name}:{0.number}'.format( tdf20))

print(tdf10.__dict__)
print(tdf20.__dict__)
# print(tdf20.shareee(tdf10))

s = str('hello Liu'); print(s, type(s))
s = 'hello Liu'; print(s, type(s))

print(Fund.self)
# __main__ experiment
print('\n===== __main__ ===========')
print(__main__.tdf10)
print(__main__.tdf10.__init__)
__main__.tdf10.__init__('TDF30', 11000063);
print(tdf20.name, tdf20.number) # no impact

# if we try to access to static java feild with instnce  its gives error
# but py does not error/warning while accessing class attribute with insatnce
# rather it adds new feild  in itance with same name.
# class attribute id differeent from static feild in java.
# quite new thing for  java OOP developer