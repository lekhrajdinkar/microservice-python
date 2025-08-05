#f1=open('/Users/lekhrajdinkar/file.txt') #absolute path
def p(*text):
    for t in text: print(*text, end='\n')

def w(text, f): print(text, file=f)

def readFile1():
    f2 = open('io/file-read-io.txt', 'r') # relative path
    for l in f2:
        if 'liu' in l:
            print(l, type(l))
    f2.close();

def readFile2():
    with open('io/file-read-io.txt', 'r') as file: # no need to close here
        for line in file: print(line, end='')
# ==========================
def readFileLineByLine(): # A. readline : reads single line
    with open('io/file-read-io.txt', 'r') as f: # no need to close here
        line = f.readline()
        while line:
            print(line, end='')
            line = f.readline()

def readFileByAllLineList(reverse: bool): # B. readlines : reads entire file as List of string/line
    with open('io/file-read-io.txt', 'r') as f: # no need to close here
        all_lines_list = f.readlines(); p(all_lines_list)
        if reverse: all_lines_list = all_lines_list[::-1]
        for line in all_lines_list: p('readFileByAllLineList ::', line);
    return all_lines_list

def readFileAllLines(reverse: bool): # C. read : reads entire file as single string
    with open('io/file-read-io.txt', 'r') as f: # no need to close here
        all_lines= f.read()
        if reverse: all_lines= all_lines[::-1]
        for line in all_lines:
            p(line)

def writeToFile():
    with open('io/write-file-io.txt', 'w') as f: # no need to close here
        for line in readFileByAllLineList(True):
            w(line,f);

def appendFile():
    with open('io/append-io.txt', 'a') as f: # no need to close here
        for line in readFileByAllLineList(False):
            w(line+" appendging...",f);

def evalDemo():
    with open('io/file-read-io.txt', 'r') as f:
        line1 = f.readline(); #print(line)
        great, name = line1.split(',') # python expression
        print(great, name)

        line2 = f.readline()
        s,n,d,l  = eval(line2) # python expression
        print(s, n, d['k1'], l[2])

# print("Strip usecase".strip('e'))
# writeToFile()
# evalDemo()
appendFile()
