import javalang

import plyj.parser
import plyj.model as m

import numpy as np
import scipy as sp
import matplotlib as mp
import matplotlib.pyplot as plt

from collections import Counter
import os, json

c_dict = None


"""
analyze
@param folder: java project folder
return void
"""
def analyze(folder,test_num):
    OUTFILE = "../visualize/output_tree" + str(test_num) + ".json"
    global c_dict
    c_dict = {}
    c_dict["name"] = "Test Project " + str(test_num)
    c_dict["children"] = []
    files = [x for x in os.listdir(folder)]
    print("Test: " + str(folder))
    #iterate through all the files in the testfolder
    for file in files:
        # c_dict["children"].append(create_blank_node(file))
        java_file = os.path.join(folder, file)
        p = plyj.parser.Parser()
        tree = p.parse_file(java_file)
        print("===packages===")
        print(tree.package_declaration)
        print("===imports===")
        print(tree.import_declarations)
        # print("===types===")
        # print(tree.type_declarations)
        print("===list of declared types===")
        for t in tree.type_declarations:
            if t.__class__.__name__ == "ClassDeclaration":
                c_dict["children"].append(get_children(t))
                # c_dict["children"][-1] = parse_class(t.name, t)
        # parse_types(java_file, tree.type_declarations)


    #write the tree dictionary to file
    f = open(OUTFILE, "w")
    f.write(json.dumps(c_dict))
    f.close()

def create_blank_node(_name):
    temp_obj = {}
    temp_obj['name'] = node.name
    return temp_obj

def get_children(node):   
    temp_obj = {}

    _name = node.__class__.__name__
    
    if _name == "ClassDeclaration":
        temp_obj['name'] = node.name + " (class)"
        body_elements = getattr(node,"body")
        temp_obj['children'] = [get_children(x) for x in body_elements]
    elif _name == "FieldDeclaration":
        temp_obj['name'] = node.variable_declarators[0].variable.name + " (variable)"
    elif _name == "MethodDeclaration":
        temp_obj['name'] = node.name + " (method)"
    return temp_obj

def parse_class(c_name, c):
    body_elements = getattr(c,"body")
    plot_token_types(c_name,body_elements)
    for b in body_elements:
        if b.__class__.__name__ == "ClassDeclaration":
            parse_class(b.name, b)






def parse_types(f_name, types):
    for t in types:
        print(t._fields)
        # for field in t._fields:
        #     print(field+"\n---")
        #     print(getattr(t,field))
        body_elements = getattr(t,"body")
        plot_token_types(f_name,body_elements)


def analyze_javalang(folder):
    files = [x for x in os.listdir(folder)]
    print("Test: " + str(folder))
    #iterate through all the files in the testfolder
    for file in files:
        print("Analyzing: " + str(file))
        f = open(os.path.join(folder, file), "r")
        text = f.read()
        tree = javalang.parse.parse(text)
        # print(tree)
        tokens = list(javalang.tokenizer.tokenize(text))
        # print(tree.package.name)
        # plot_token_types(file, tokens)
        token_values = [t.value for t in tokens]
        for t in tokens:
            print(t)





"""

Visualization Helper Functions

"""



def plot_token_types(_name,tokens):
    counter = Counter([x.__class__.__name__ for x in tokens]).most_common()
    print(_name + ": " + str(counter))
    token_names, token_counts = zip(*counter[::-1])

    # Plot histogram using matplotlib barh().
    indexes = np.arange(len(token_names))
    width = 1
    plt.figure(figsize=(16,9))
    plt.barh(indexes, token_counts, width)
    plt.yticks(indexes + width * 0.5, token_names)
    plt.xlabel("Frequency")

    plt.title(str(_name) + " Composition")
    plt.grid(True)
    plt.show()


#TODO: Add more functions for the pyreflect module

