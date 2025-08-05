dict_with_mutable_value={
    'app1': ['java', 'angular'],
    'app2': ['python', 'react']
}
dict_with_immutable_value={
    'app1': 'java',
    'app2': 'python'
}

cgc = None
cgc_copy = None

def update_immutable_feild(d: dict):
    d['app1'] = 'Java8'

def update_mutable_feild(d: dict):
    d['app1'].append('oracle')

def update_and_print(mode: str, d: dict, dc: dict):
    if mode == 'm':
        update_mutable_feild(d)
    else:
        update_immutable_feild(d)
    print(dc); print(cgc);


def clear_dict(mode: str, d: dict, dc: dict):
    if mode == 'm':
        print('clearing with mode m')
        d = dict_with_mutable_value;
    else:
        print('clearing with mode im')
        d = dict_with_immutable_value;
    dc = None;

def copy_ref( mode: str, d: dict, dc: dict):
    clear_dict(mode, d, dc)
    print('-'*10, 'ref', '-'*10)
    dc = d
    update_and_print(mode, d, dc)

def shallow_copy(mode: str, d: dict, dc: dict):
    clear_dict(mode, d, dc)
    d = dict_with_mutable_value;
    print('-' * 10, 'shallow copy()', '-' * 10)
    dc = d.copy()
    update_and_print(mode, d, dc)

def deep_copy(mode: str):
    pass

# =========== MAIN RUN ++++++

#copy_ref('m', cgc, cgc_copy)

shallow_copy('m', cgc, cgc_copy)