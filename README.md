# cs230project
Design Project repository for software engineering course.

Pyreflect
===

A reflection module for Java written in Python

How to Run
===

View Project Tree
---
1. Run the runtests.py script from the pyreflect folder.
2. Example output from test project 1 (within the tests folder) will be loaded into a json tree
3. Open the file visualize/tree.html to visualize the project structure


Run Code Sniffing Tool
---

### Method has too many Commands, ex: ./pyreflect.py -f ../tests/old/proj1 -lm 5
### Method has too many Parameters, ex: ./pyreflect.py -f ../tests/old/proj1 -lp 2

options:
-f (path to test folder)
-lm N (long method test with max N commands)
-lp N (long parameter test with max N parameters)

Requirements
===
javalang: https://github.com/c2nes/javalang
http://modeling-languages.com/uml-tools/#python