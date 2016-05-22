# import plyj.parser
# import plyj.model as m
import os, json, sys
import sys, argparse, time
import random
# import numpy as np
# import scipy as sp
# import matplotlib as mp
# import matplotlib.pyplot as plt

from collections import Counter

"""
nodeutil.py
Collection of Helper functions used for detecting code smells

"""


"""
GOD CLASS THRESHOLD VALUES
"""
# * Very high threshold for WMC (Weighted Method Count).
 # * See: Lanza. Object-Oriented Metrics in Practice. Page 16.
WMC_VERY_HIGH = 47
WMC_OBJECTS = ["MethodDeclaration", "ConditionalOr", "ConditionalAnd", "IfThenElse", "While", "DoWhile", "SwitchCase", "For", "Try", "Catch", "Conditional"]

 # * Few means between 2 and 5.
 # * See: Lanza. Object-Oriented Metrics in Practice. Page 18.
FEW_THRESHOLD = 5

 # * One third is a low value.
 # * See: Lanza. Object-Oriented Metrics in Practice. Page 17.
ONE_THIRD_THRESHOLD = 1/3.0
#self.trees contains all the java file parse trees indexed by filename
""" 
END GOD CLASS THRESHOLD VALUES
"""

#@param node: node is a method AST node

def is_foreign_access(node):
    """
    @param node: node is a method AST node
    @return: boolean representing if node is a setter or getter to a foreign element
    """
    return random.choice([True, False])

#@param node: node is a method AST node
def is_foreign_call(node):
    """
    @param node: node is a method AST node
    @return: boolean representing if node is a foreign method call
    """
    return random.choice([True, False])

#@param m: m is a method AST
def wmc_count(m):
    count = 1
    return count

def count_method_pairs(methods):
    for m in methods:
        print("%s: %s" % (m.name, str(m)))
    return 0

def print_to_log(txt):
    with open("./log.txt","a+") as f:
        f.write(txt+"\n")

def check_god_class(c,k):
    """
    @param c: class AST object
    @param k: file name
    @return: boolean representing if c is a god class
    """
    #wmc: weighted method count
    wmc = 0 
    #atfd: count of foreign method accesses
    atfd = 0 
    #tcc: measure of method coupling - The relative number of method pairs of a class that access in common at least one attribute of the measured class [BK95]
    tcc = 0 

    method_pairs = 0#used for tcc calculation

    #extract the class method and attribute declarations
    class_body = c.body
    methods = []
    attrs = []

    for x in class_body:
        cn = x.__class__.__name__
        if cn == "MethodDeclaration":
            methods.append(x)
        elif cn == "VariableDeclaration":
            try:
                attrs.extend([v.variable.name for v in x.variable_declarators])
            except:
                continue

    # print_to_log(str(methods))
    num_methods = len(methods)
    total_method_pairs = num_methods * (num_methods - 1) / 2.0;
    method_names = [x.name for x in methods]
    # method_pairs = count_method_pairs(methods)

    #calculate wmc and atfd by visiting each method node
    for i in range(num_methods):
        method_i = methods[i]
        method_body = method_i.body
        if method_body:
            for b in method_body:
                    if is_foreign_call(b) or is_foreign_access(b):
                        atfd += 1
                    if b.__class__.__name__ in WMC_OBJECTS:
                        wmc += wmc_count(b)

        for j in range(i+1, num_methods):
            method_j = methods[j]
            method_pairs += random.choice([0,1])
            

    #calculate tcc 
    if total_method_pairs>0:
        tcc = 1#method_pairs / total_method_pairs
    else:
        tcc = 0



    if (wmc >= WMC_VERY_HIGH and atfd > FEW_THRESHOLD and tcc > ONE_THIRD_THRESHOLD):
        print("%s: %s God Class (WMC=%d, ATFD=%d, TCC=%d/%d)" % (k, c.name, wmc, atfd, method_pairs, total_method_pairs))
        return True
    else:
        #print here used for debug of non god classes
        # print("%s: %s Not God Class (WMC=%d, ATFD=%d, TCC=%d)" % (k, c.name,wmc, atfd, tcc))
        return False

"""

Helper functions for code smell detection

"""

#@param methods: methods is a list of method AST objects
#returns similarity of methods
def method_similarity(method1, method2):
    #returns if two methods are sufficiently similar to be refactored

    body1 = method1.body
    body2 = method2.body
    if body1 is None or body2 is None:
        return 0

    # if abs(len(body1) - len(body2)) > 3:
    #     return 0 #not similar
    body1 = set([str(x) for x in body1])
    body2 = set([str(x) for x in body2])
    similarity_score = len(body1.intersection(body2))
    # print("Similarity %s/%s: %d" % (method1.name, method2.name, similarity_score))
    return similarity_score


def get_parameter_length(method):
    #number of parameters in the method call
    return len(method.parameters) 


def get_class_length(c):
    #number of declarations in the class body
    return len(c.body)


def get_method_length(method):
    body_elements = method.body
    if body_elements is None:
        return 0
    c = 0
    # return len(body_elements) #false

    for node in body_elements:
        _name = node.__class__.__name__
        if _name == "IfThenElse":
            if hasattr(node, "if_true"):
                if node.if_true.__class__.__name__ == "Block":
                    c += len(node.if_true.statements)
                else:
                    c+=1
            if hasattr(node, "if_false"):
                if node.if_false.__class__.__name__ == "Block":
                    c += len(node.if_false.statements)
                else:
                    c+=1
        elif _name == "Switch":
            if node.switch_cases is not None:
                for case in node.switch_cases:
                    c+=len(case.body)


        else: #other basic body element type (that doesn't have inner body)
            c+=1

    return c


def get_node_name(i_name, c_name):
    return i_name + " (" + c_name + ")" 

def get_children(node):   
    #recursively iterates through node children in order to construct json object
    temp_obj = {}
    _name = node.__class__.__name__
    
    if _name == "ClassDeclaration":
        temp_obj['name'] = get_node_name(node.name,"Class")
        body_elements = getattr(node,"body")
        if body_elements is not None:
            temp_obj['children'] = [get_children(x) for x in body_elements]
    elif _name in ["FieldDeclaration","VariableDeclaration"]:
        temp_obj['name'] = get_node_name(",".join([x.variable.name for x in node.variable_declarators]), "Field")
    elif _name == "MethodDeclaration":
        temp_obj['name'] = get_node_name(node.name,"Method")
        body_elements = getattr(node,"body")
        if body_elements is not None:
            temp_obj['children'] = [get_children(x) for x in body_elements]
    elif _name == "IfThenElse":
        temp_obj['name'] = _name
        if hasattr(node, "if_true"):
            temp_obj['children'] = []
            if node.if_true.__class__.__name__ == "Block":
                temp_obj['children'].append({"name": "if_true", "children": 
                    [get_children(x) for x in node.if_true.statements]})
        if hasattr(node, "if_false"):
            if node.if_false.__class__.__name__ == "Block":
                temp_obj['children'].append({"name": "if_false", "children": [get_children(x) for x in node.if_false.statements]})
    elif _name == "Return":
        pass
    else: #other class types (default behavior)

        if hasattr(node, "name"):
            temp_obj['name'] = get_node_name(node.name,_name)
        else:
            temp_obj['name'] = _name

        # if _name == "Return":
        #     if hasattr(node, "result"):
        #         # temp_obj['children'] = [get_children(node.result)]
        #         temp_obj['name'] += "(" + str(node.result.name) + ")"
        # elif _name == "Assignment":
        #     if hasattr(node, "rhs"):
        #         # temp_obj['children'] = [get_children(node.rhs)]
        #         temp_obj['name'] += "(" + str(node.rhs.name)+ ")"
        if _name in ["For", "DoWhile", "While"]:
            body_elements = getattr(node,"body")
            if body_elements is not None:
                temp_obj['children'] = [get_children(x) for x in body_elements]


    return temp_obj

def get_file_name(f):
    return os.path.basename(f)


