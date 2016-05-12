s# cs230project
Design Project repository for software engineering course.

Pyreflect
===

A reflection module for Java written in Python

Command Line Interface
---

### Method has too many Commands
ex: ./pyreflect.py -f ../tests/old/proj1 -lm 5

#####options:
###### -f (path to test folder),
###### -lm N (long method test with max N commands)

### Method has too many Parameters
ex: ./pyreflect.py -f ../tests/old/proj1 -lp 2

#####options:
###### -f (path to test folder),
###### -lp N (long parameter test with max N parameters)

#### Other Options
###### -g: Look for God Classes
###### -lc: Lazy Class - expects minimum statement amount parameter
###### -d: Duplicate Code - expects minimum line similarity amount parameter
###### -a: Run all 5 tests (long method, long parameter, lazy class, duplicate code, god class) on project with default parameters.
###### -t: Print time for parse and test(s) execution 


<!-- # Website -->
Render Visualizations
---

From website directory.

1. Run the runtests.py script from the pyreflect folder.

For first time configuration, run the following

1. bower install
2. gulp bower
3. gulp build

Gather generated project json files and load into the app/trees folder.
Json files should be named tree{N}.json
Start a localhost server to view the visualization webpage (gulp serve from root folder would work for this).

Examples
---

See tests folder.


Requirements
---

## For Command Line Pyreflect tool
<!-- http://modeling-languages.com/uml-tools/#python -->
###### python 2.7 or newer
###### scipy, numpy, matplotlib
###### plyj: https://github.com/musiKk/plyj

## For Visualization website

###### node/npm
###### bower
<!-- gulp -->