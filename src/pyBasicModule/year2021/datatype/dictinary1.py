from ..common_data import data,print_color
from ..others import copy1

project = data.project
project_tect_stack = data.project_tect_stack

def print_project():
    for p_key in project:
        print(f"{p_key} - {project[p_key]}")
    print('a - Add new project','\ne - EXIT', )

def print_project_tech(dict):
    for index, p_key in enumerate(dict):
        print( p_key,' : ', dict[p_key])

def add_project():
    k = input('Enter project code: ')
    v = input('Enter project namne : ')
    tech = input('Enter tech stack')
    tech = tech.split(',')
    data.project.setdefault(k, v)
    data.project_tect_stack.setdefault(v, tech)

# Exercise 1
def deep_copy_dict(d: dict):
    return copy1.deepcopy(d)
def shallow_copy_dict(d: dict):
    return d.copy()

d1 = data.config_dict;
d2 = deep_copy_dict(d1); print(id(d1.get('os')), id(d2.get('os')))

d1 = data.config_dict;
d2 = shallow_copy_dict(d1); print(id(d1.get('os')), id(d2.get('os')))

# Exercise 2 prg
while True:
    print(('=' * 20), 'welcome', ('=' * 10) * 2)
    print_project(); choice = input('Enter valid project code : ')
    if choice in project:
        tech = project_tect_stack[project[choice]]
        # IMP1, create new dic: comprehension
        tech_dict = { str(index + 1):value for index,value in enumerate(tech) }
        print(f'Technology stack for {project[choice]}')
        print_project_tech(tech_dict)
        print(dict(tech_dict.items()))
        #for kk in tech_dict.keys(): print(kk)
        #for kk in tech_dict.values(): print(kk)

        fav = None
        # IMP2, : in with for/while and if
        while fav not in tech_dict:
            fav = input('Enter your preferred Technology: ')
            if fav in tech_dict:
                print_color.myPrintWithMoreEffect(tech_dict[fav] + ' is nice choice !!', print_color.UNDERLINE,
                                                  print_color.BOLD, print_color.GREEN)
                print(f'Checking related project for {tech_dict[fav]}')
                if tech_dict[fav] in data.related_project:
                    print('Found :: ', data.related_project[tech_dict[fav]])
                else:
                    print('No project found !! Explore below option :')
                    for k,v in data.related_project.items():
                        print(k.center(30),v,sep=' >>> ')
    elif choice == 'e':
        break
    elif choice == 'a':
        add_project()






