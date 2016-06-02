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
STANDARD_TYPES = ["float","int", "integer", "char", "character", "double", "string","byte", "array", "bool", "boolean"]

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

def is_foreign_access(node):
    """
    @param node: node is a method AST node
    @return: boolean representing if node is a setter or getter to a foreign element
    """
    try:
        return node.__class__.__name__ == "FieldDeclaration" and str(node.type.name).lower() not in STANDARD_TYPES
    except Exception as e:
        print(str(e))
        return False

def is_foreign_call(node):
    """
    @param node: node is a method AST node
    @return: boolean representing if node is a foreign method call
    """
    return node.__class__.__name__ == "MethodInvocation" and any(["get","is","set"] in str(node.name).lower())
    # return random.choice([True, False])


def wmc_count(node):
    """
    @param node: node is a method AST node
    @return: weighted method count for the node
    """
    if node.__class__.__name__ in WMC_OBJECTS:
        if hasattr(node,"body"):
            return 1 + wmc_count(node)
        else:
            return 1
    else:
        return 0

def count_method_pairs(methods):
    """
    @param methods: number of methods in the class
    @return: number of possible method pairs
    """
    for m in methods:
        print("%s: %s" % (m.name, str(m)))
    return 0

def print_to_log(txt):
    with open("./log.txt","a+") as f:
        f.write(txt+"\n")

def shared_attr_access(method1,method2):
    """
    @param m1,m2: method AST nodes
    @return: bool representing if m1 and m2 share an attribute access
    """
    m1_body = method1.body
    m2_body = method2.body
    if len(m1_body) == 0 or len(m2_body) == 0:
        return False

    for m1 in m1_body:
        if m1.__class__.__name__ == "Assignment":
            lhs1 = m1.lhs.name
            rhs1 = m1.rhs.name
            for m2 in m2_body:
                if m1.__class__.__name__ == "Assignment":
                    lhs2 = m2.lhs.name
                    rhs2 = m2.rhs.name
                    if lhs1 == lhs2 or lhs1 == rhs2 or rhs1 == lhs2 or rhs1 == rhs2
                        return True

    return False
    # return random.choice([True, False])

def check_god_class(c,k):
    """
    @param c: class AST object
    @param k: file name key
    @return: boolean representing if c is a god class
    """
    #wmc: weighted method count
    wmc = 0 
    #atfd: count of foreign method accesses
    atfd = 0 
    #tcc: measure of method coupling - 
    #The relative number of method pairs of a class that access in common at least one attribute of the measured class [BK95]
    tcc = 0 

    method_pairs = 0

    #extract the class method and attribute declarations
    class_body = c.body
    methods = []
    attrs = []

    class_name = c.name


    #derive the method count for the class
    for x in class_body:
        cn = x.__class__.__name__
        if cn == "MethodDeclaration":
            methods.append(x)
        elif cn == "VariableDeclaration":
            try:
                attrs.extend([v.variable.name for v in x.variable_declarators])
            except:
                continue

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
                    wmc += wmc_count(b)

        for j in range(i+1, num_methods):
            method_j = methods[j]
            if shared_attr_access(method_i, method_j):
                method_pairs += 1

    #calculate tcc 
    if total_method_pairs>0:
        tcc = method_pairs / total_method_pairs
    else:
        tcc = 0

    if (wmc >= WMC_VERY_HIGH and atfd > FEW_THRESHOLD and tcc > ONE_THIRD_THRESHOLD):
        print("%s: %s Possible God Class (WMC=%d, ATFD=%d, TCC=%d/%d=%d)" % (k, c.name, wmc, atfd, method_pairs, total_method_pairs,tcc))
        return True
    else:
        #print here used for debug of non god classes
        # print("%s: %s Not God Class (WMC=%d, ATFD=%d, TCC=%d)" % (k, c.name,wmc, atfd, tcc))
        return False

"""
Helper functions for code smell detection
"""

def method_similarity(method1, method2):
    """
    #@param methods: methods is a list of method AST objects
    #returns if two methods are sufficiently similar to be refactored
    """
    body1 = method1.body
    body2 = method2.body
    if body1 is None or body2 is None:
        return 0

    body1 = set([str(x) for x in body1])
    body2 = set([str(x) for x in body2])
    similarity_score = len(body1.intersection(body2))

    return similarity_score

def get_parameter_length(method):
    #number of parameters in the method call
    return len(method.parameters) 

def get_class_length(c):
    #number of declarations in the class body
    return len(c.body)

def get_method_length(method):
    #length of method (including nested nodes)
    body_elements = method.body
    if body_elements is None:
        return 0

    c = 0

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


