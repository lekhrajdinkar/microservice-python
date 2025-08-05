# from cyclic_import_m1 import func_from_m1   # cyclic import

def func_from_m2():
    from cyclic_import_m1 import func_from_m1  # fix
    print("m2 calls m1:")
    func_from_m1()

