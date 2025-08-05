def case_a() -> str:
    print(f"Handled caseA ©️")
    return "A"
def case_b() -> str:
    print(f"Handled caseB ©️")
    return "B"
def default() -> str:
    print(f"Handled default ©️")
    return "Default"

switch: dict = {
    'a': case_a,
    'b': case_b,
    'default': default
}

#value = 'a'
#print(switch.get(value, default)())
