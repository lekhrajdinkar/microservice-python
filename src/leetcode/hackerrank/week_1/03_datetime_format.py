def timeConversion_v2(s):
    s_arr = s.split(":")
    hh = s_arr[0]
    mm = s_arr[1]
    ss = s_arr[2][:2]
    ampm = s_arr[2][2::]
    result = ''

    if ampm == 'AM':
        result= ":".join([ f"{str(int(hh) % 12):02}", mm, ss])
    else:
        result= ":".join([ str((int(hh)%12)+12), mm, ss ])

    print(result)


if __name__ == '__main__':
    t1 = '12:05:45AM'
    t2 = '07:05:45PM'

    timeConversion_v2(t1)
    timeConversion_v2(t2)
