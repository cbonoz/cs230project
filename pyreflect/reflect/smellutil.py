# import plyj.parser
# import plyj.model as m
import os, json, sys
import sys, argparse, time
import random, traceback
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
WMC_OBJECTS = ["methoddeclaration", "conditionalor", "conditionaland", "ifthenelse", "While", "dowhile", "switchcase", "for", "try", "catch", "conditional","throws","foreach", "assignment","methodinvocation"]
STANDARD_TYPES = ["float","int", "integer", "char", "character", "double", "string","byte", "array", "bool", "boolean"]
ACCESSOR_LIST = ["get","is","set","check"]

 # * Few means between 2 and 5.
 # * See: Lanza. Object-Oriented Metrics in Practice. Page 18.
FEW_THRESHOLD = 3

 # * One third is a low value.
 # * See: Lanza. Object-Oriented Metrics in Practice. Page 17.
ONE_THIRD_THRESHOLD = 1/3.0
#self.trees contains all the java file parse trees indexed by filename
""" 
END GOD CLASS THRESHOLD VALUES
"""

def is_foreign_access(node):
    """
    for atfd
    @param node: node is a method AST node
    @return: boolean representing if node is a setter or getter to a foreign element
    """
    try:
        if node.__class__.__name__ in ["FieldDeclaration", "Assignment"]:
            # return str(node.type.name).lower() not in STANDARD_TYPES
            return str(get_object_name(node)).lower() not in STANDARD_TYPES
    except Exception as e:
        print(str(e))
    return False

def is_foreign_call(node):
    """
    for atfd
    @param node: node is a method AST node
    @return: boolean representing if node is a foreign method call
    """
    try:
        if node.__class__.__name__ == "MethodInvocation":
            m_name = str(get_object_name(node)).lower()
            return any(substring in m_name for substring in ACCESSOR_LIST)
    except Exception as e:
            print(str(e))
    return False

    # return random.choice([True, False])


def wmc_count(node):
    """
    @param node: node is a method AST node
    @return: weighted method count for the node
    """
    is_wm = 1 if node.__class__.__name__.lower() in WMC_OBJECTS else 0

    if hasattr(node,"body"):
        return is_wm + sum([wmc_count(x) for x in node.body])
    return is_wm


def atfd_count(node):
    if hasattr(node,"body"):
        return 1 + sum([atfd_count(x) for x in node.body])
    return 1 if (is_foreign_call(node) or is_foreign_access(node)) else 0


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

def get_object_name(n):
    if hasattr(n,"value"):
        return n.value
    elif hasattr(n,"name"):
        return n.name
    elif hasattr(n,"type"):
        if hasattr(n.type,"name"):
            return n.type.name
        else:
            return None
    elif hasattr(n,"lhs"):
        return get_object_name(n.lhs)
    else:
        return None



def shared_attr_access(method1,method2):
    """
    @param m1,m2: method AST nodes
    @return: bool representing if m1 and m2 share an attribute access
    """
    m1_body = method1.body
    m2_body = method2.body



    if m1_body is None or m2_body is None:
        return False


    for node1 in m1_body:
        try:
            n1_name = get_object_name(node1)
            if not n1_name:
                continue

            for node2 in m2_body:
                n2_name = get_object_name(node2)
                if not n2_name:
                    continue
                if n1_name == n2_name:
                    return True
        except Exception as e:
            print(traceback.format_exc())
            print(str(e))
            sys.exit(1)
    
    return False
    # return random.choice([True, False])

def check_god_class(c,fname):
    """
    @param c: class AST object
    @param fname: file name key
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
                atfd += atfd_count(b)
                wmc += wmc_count(b)

        for j in range(i+1, num_methods):
            method_j = methods[j]
            if shared_attr_access(method_i, method_j):
                method_pairs += 1

    #calculate tcc 
    if total_method_pairs>0:
        tcc = (float(method_pairs) / total_method_pairs)
    else:
        tcc = 0

    if (wmc >= WMC_VERY_HIGH and atfd > FEW_THRESHOLD and tcc < ONE_THIRD_THRESHOLD):
        # print("%s: %s Possible God Class" % (fname, c.name))
        print("%s: %s Possible God Class (WMC=%d, ATFD=%d, TCC=%d/%d=%.2f)" % (fname, c.name, wmc, atfd, method_pairs, total_method_pairs,tcc))
        return True
    else:
        #print here used for debug of non god classes
        # print("%s: %s Not God Class (WMC=%d, ATFD=%d, TCC=%d/%d=%.2f)" % (fname, c.name,wmc, atfd, method_pairs, total_method_pairs,tcc))
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
    if c.body:
        return len(c.body)
    return 0

def get_method_length(method):
    #length of method (including nested nodes)
    if method is None:
        return 0

    _name = method.__class__.__name__
    try:
        if hasattr(method, "body"):
            if method.body:
                return 1 + sum([get_method_length(x) for x in  method.body])
            return 0
        elif hasattr(method, "switchcases"):
            if method.switchcases:
                return 1 + sum([get_method_length(x) for x in  method.switchcases])
            return 0
        elif _name == "IfThenElse":
            true_length = 0
            if method.if_true:
                true_length = 1
                if hasattr(method.if_true, "statements"):
                    true_length = 1 + sum([get_method_length(x) for x in method.if_true.statements])

            false_length = 0
            if method.if_false:
                false_length = 1
                if hasattr(method.if_false, "statements"):
                    false_length = 1 + sum([get_method_length(x) for x in method.if_false.statements])

            return true_length + false_length
    except Exception as e:
        print(method)
        print("ERROR: " + str(e))
        print(traceback.format_exc())
        sys.exit(1)

    return 1


#Text Labels for tree nodes
def get_node_name(i_name, c_name):
    return i_name + " (" + c_name + ")" 

def get_type(node_type):
    if hasattr(node_type, "name"):
        if hasattr(node_type.name, "value"):
            return str(node_type.name.value)
        return str(node_type.name)
    return str(node_type)


def get_children(node):   
    #recursively iterates through node children in order to construct json object
    temp_obj = {}
    _name = node.__class__.__name__
    
    #check core elements
    if _name == "ClassDeclaration":
        temp_obj['name'] = get_node_name(node.name,"Class")
        body_elements = getattr(node,"body")
        if body_elements is not None:
            temp_obj['children'] = filter(lambda x: x != {}, [get_children(x) for x in body_elements])
    elif _name in ["FieldDeclaration","VariableDeclaration"]:

        temp_obj['name'] = get_node_name(get_type(node.type)  + " " + ",".join([x.variable.name for x in node.variable_declarators]), "Field")

    elif _name == "MethodDeclaration":
        temp_obj['name'] = get_node_name(get_type(node.return_type) + " " + node.name,"Method")
        body_elements = getattr(node,"body")
        if body_elements is not None:
            temp_obj['children'] = filter(lambda x: x != {}, [get_children(x) for x in body_elements])

    elif _name == "Return":
        if hasattr(node, "result"):
            if hasattr(node.result, "name"):
                temp_obj['name'] = get_node_name(node.result.name, "Return")

        # print("Created return obj: " + str(temp_obj))
    elif _name == "VariableDeclaration":
        temp_obj['name'] = get_node_name(node.variable.name,"Variable")

    else: #other class types (default behavior)

        #assign name
        if hasattr(node, "name"):
            temp_obj['name'] = get_node_name(node.name,_name)
        else:
            temp_obj['name'] = _name

        #assign children
        if _name in ["For", "DoWhile", "While", "SwitchCase"]:
            body_elements = getattr(node,"body")
            if body_elements is not None:
                temp_obj['children'] = filter(lambda x: x != {}, [get_children(x) for x in body_elements])
        elif _name == "IfThenElse":
            if hasattr(node, "if_true"):
                temp_obj['children'] = []
                if node.if_true.__class__.__name__ == "Block":
                    temp_obj['children'].append({"name": "if_true", "children": 
                        filter(lambda x: x != {}, [get_children(x) for x in node.if_true.statements])})
            if hasattr(node, "if_false"):
                if node.if_false.__class__.__name__ == "Block":
                    temp_obj['children'].append({"name": "if_false", "children": 
                        filter(lambda x: x != {}, [get_children(x) for x in node.if_false.statements])})


    return temp_obj

def get_file_name(f):
    return os.path.basename(f)


