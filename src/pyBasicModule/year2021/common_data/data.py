#array of tuple
albums_list = [
    ('Eminem', 2000, ['my mom', 'iam not afraid']),
    ('Selena', 2010, ['heart', 'same old love', 'sad']),
    ]

config_list = ['os', 'memory', 'system', 'model', 'year']
config_dict = dict.fromkeys(config_list, 'dummyValue')

config_dict_init = {
    'os': 'mac',
    'memory': '16GB',
    'system': '64-bit',
    'year': 2025,
    'model': None
}
config_dict_init.popitem()  # ⬅️
config_dict.update(config_dict_init) # ⬅️

# dictionary = JavaScript object literal
project = {
    '1': 'app1',
    '2' : 'app2'
}
project_tect_stack = {
    'app1': ['java', 'angular', 'spring-boot', 'hibernate', 'rest-api'],
    'app2': ['java', 'jsp', 'thyme-leaf']
}
related_project = {
    'java': ['CSTAR'],
    'angular': ['CARS']
}

# suitable keys for dict - immutable, and hashable ⬅️
t1 = 'java',10,2020
t2 = 'python',3,[2020, 2021]  # TypeError: unhashable type: 'list'
t3 = 'nodeJs','10',2020
dict1={ t1: 'value1', t3: 'value2' }


menu = [
    ["boba tea", 'moon cake', 'spam'],
    ["boba tea", 'bun', 'casetella', 'spam'],
    ['moon cake', 'bun', 'casetella'],
    ["boba tea", 'moon cake', 'casetella'],
]


