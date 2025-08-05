# cd .\src\pyBasicModule\year2025\ 🏃‍♂️
# python -m main2025
# root path: C:\Users\Manisha\Documents\GitHub\idea\02-etl-pyspark\src\pyBasicModule\year2025\
app_name = "python demo 2025"
from src.pyBasicModule.year2025.datatype import main as datatype_main
from src.pyBasicModule.year2025.datatype import dict1, list_and_iterable1 as list1, byte1,formating1,sequence03,tuple1
from src.pyBasicModule.year2025.others import custom_switch
from src.pyBasicModule.year2025.datatype import str1
from src.pyBasicModule.year2025.module import  date_time_calender

def test_datatype1():
    datatype_main.typeDemo()
    datatype_main.printCurrentModule()
    datatype_main.printOtherModule_static()
    datatype_main.printOtherModule_dynamic("src.pyBasicModule.year2025.datatype.sequence03")

def test_datatype2():
    str1.str_all()
    str1.str_all_2()
    byte1.byteDemo()

def test_collection():
    dict1.dictDemo()
    list1.listDemo()
    list1.comprehension_demo()
    list1.generation_demo()
    tuple1.tuple_demo()
    sequence03.listOperations()
    sequence03.strOperations()
    sequence03.strOperations_negative_indexing()

def test_custom_switch():
    custom_switch.switch.get("a")()
    custom_switch.switch.get("b")()
    custom_switch.switch.get("default")()

def test_formatting():
    formating1.formatingDemo1()
    formating1.p("sfdsfds","sfsdfds","mjhkmhj")

def test_file_reading():
    #gen = list1.read_file_by_line_generator_1()
    gen = list1.read_file_by_line_generator_2("src/pyBasicModule/year2025/datatype/bigfile.txt")
    for line in gen:
         print(line)

if __name__ == "__main__":
    print(f"hello {app_name}")
    test_datatype1()
    test_datatype2()
    test_collection()
    test_formatting()
    test_custom_switch()
    test_file_reading()
    list1.global_built_in() # ⬅️
    date_time_calender.datetimeCal_demo_1()





