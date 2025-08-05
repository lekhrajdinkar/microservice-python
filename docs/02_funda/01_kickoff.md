# python 3.x (since 2008)
## 1 py::Intro
- **high-level**
- open-source and cross-platform programming language
- Rapid Prototyping with REPL : Python shell + Jupyter
- Strong Community and Documentation
- **interpreted** 
    - processed at runtime by the interpreter.
    - do not need to compile your program
- **OOPS, functional, procedural**
- extensive lib (built-in / 3rd party)

---
## 2 py::usage
- Web development
- Data Science 
- machine learning
- Job scheduling, Automation and scripting
- ETl (pySpark)
- **more**
    - Desktop GUI Applications
    - Console-based Applications
    - Game Development

---
## 3 py::install and run
-  https://www.python.org/
- update env var:  PATH, PYTHONPATH, PYTHONHOME
```shell
sudo apt-get install python3.11
sudo yum install python3
```
- linux: Python's executable is installed in **/usr/bin/** directory
- windows:   **C:\python311**
- REPL : py enter, then >>> prompt will come. quit()
- run : **python3 prog-1.py**
- **Shebang** 
    - #! /usr/bin/python3.11
    - script itself can be a self executable in Linux, like a shell script
    - run directly: ./prog-1.py
  
- ![img.png](99_IMG/001/img.png)

---
## 4 py::venv
- system-wide installation done above.
- need isolated environments of Python, for diff appl.
- **python3 -m venv myvenv**
- myvenv\scripts\**activate**
- ![img_1.png](99_IMG/001/img_1.png)

## 5. py::reserved keyword
```
and	as	assert
break	class	continue
def	del	elif
else	except	False
finally	for	from
global	if	import
in	is	lambda
None	nonlocal	not
or	pass	raise
return	True	try
while	with	yield
```
