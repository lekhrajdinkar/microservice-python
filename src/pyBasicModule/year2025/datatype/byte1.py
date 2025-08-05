"""
| Feature   | `bytes`        | `bytearray` | `memoryview`                  |
| --------- | -------------- | ----------- | ----------------------------- |
| Mutable   | ❌ No           | ✅ Yes       | ✅ Yes (if source is mutable)  |
| Use case  | Safe read-only | Modifiable  | Efficient slice/view handling |
| Copy-free | ❌              | ❌           | ✅ (no data copied)            |
"""
def byteDemo():
    b = bytes([65, 66, 67])  # ASCII codes for 'A', 'B', 'C'
    print(b)        # b'ABC'
    b[0]            # 65
    # b[0] = 90     # ❌ Error: 'bytes' object does not support item assignment
    print(type(b))

    b1 = b'lekhraj';
    for i in b1: print(f"🏃‍♂️byte:",i);
    int_arr = [ ii for ii in b1]; print("int_arr : ",int_arr)

    ba = bytearray([65, 66, 67])
    print(ba)       # bytearray(b'ABC')
    ba[0] = 90
    print(ba)       # bytearray(b'ZBC') — 'A' changed to 'Z'

    data = bytearray(b'hello')
    mv = memoryview(data)
    print(mv[0])       # 104 (ASCII for 'h')
    mv[0] = 72         # change 'h' to 'H'
    print(data)        # bytearray(b'Hello') — original data changed!





