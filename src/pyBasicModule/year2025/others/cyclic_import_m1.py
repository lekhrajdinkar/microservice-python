# from cyclic_import_m2 import func_from_m2 # cyclic import

def func_from_m1():
    from cyclic_import_m2 import func_from_m2  # FIX
    print("m1 calls m2")
    func_from_m2()