


Pyreflect
===
##### Design Project repository for software engineering course (cs230 Spring 2016)

A reflection module for Java written in Python

**Command Line Interface**
---

#### For Command Line help

pyreflect -h
<!-- ./pyreflect -h -->

#### Examples

##### Detect methods in java files (within tests/code-smell-medium/ folder) that have more than 3 statements
ex: pyreflect tests/code-smell-medium/ -lm 3

##### Detect methods in java files that have more than 2 parameters
ex: pyreflect tests/code-smell-medium/ -lp 2

##### Run a test with verbose performance time measure (add -t option)
ex: pyreflect tests/code-smell-medium/ -lp 2 -t

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

##### For Command Line Pyreflect tool
<!-- http://modeling-languages.com/uml-tools/#python -->
* python 2.7
<!-- * scipy, numpy, matplotlib -->
* plyj: https://github.com/musiKk/plyj

##### For Visualization website

* node/npm
* bower
<!-- gulp -->


To Install (installing won't modify your path)
----------

1. Git clone this repository
2. **sudo python setup.py install --record files.txt** from project home directory
3. **pyreflect -h** from command line. 


If install successful, but pyreflect not found. Run these commands
1. echo alias pyreflect=\\'python -m pyreflect.pyreflect\\' >> ~/.bash_profile. 
2. source ~/.bash_profile