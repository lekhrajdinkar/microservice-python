# == 2021 ====

from time import gmtime, localtime, time, sleep

# time.struct_time --> named tuple
def time_demo_1():
    print(gmtime(0), localtime(0))
    current_sec = time(); second_in_day = 86400;
    print('\nprevious day (LOCAL) -', localtime(current_sec - second_in_day),)
    print('\ntoday, (LOCAL) -', localtime(), localtime(current_sec), sep='\n') # both are same
    print('\nCurrent second since 1970 : ', current_sec)
    print('\ntoday, (GMT)', gmtime(current_sec)) #current time in sec since 1970

    # Access named tuple
    local_time = localtime()
    print("localtime()",local_time[0], local_time.tm_year, local_time.tm_mon, local_time.tm_zone, sep="\n ---") # access named-tuple with name or index

# string_from_time
def exercise_1():
    from time import strftime as string_from_time
    timer = input('Enter stop time in seconds __ ')
    print(f'Now, wait for {timer} seconds...')
    start_time = time();
    sleep(int(timer));
    stop_time = time()
    print( 'Date: ', string_from_time('%x', localtime(start_time)).center(50))
    print( 'start TIME : ', string_from_time('%X', localtime(start_time)))
    print( 'stop  TIME : ', string_from_time('%X', localtime(stop_time)))

    p( 'weekday  : '+ string_from_time('%a')) # %A
    p( 'Month  : '+ string_from_time('%B')) # %b
    p( 'Date and time  : '+ string_from_time('%c')) #TypeError: can only concatenate str (not "list") to str
    p( 'Day of the year  : '+ string_from_time('%j')) #
    p( 'Time zone : '+ string_from_time('%z')) # %Z,%z ::  IST = GMT + 05:30
    p( 'other/try here : '+ string_from_time('%p')) #

# ========= print util
def p(*t):
    for text in t:
        print(text, end='\n'+('_'*50)+'\n')

if __name__ == "__main__":
    time_demo_1()
    #exercise_1()