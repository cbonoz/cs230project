import javalang
import plyj.parser
import plyj.model as m
import os, json, sys
import numpy as np
import scipy as sp
import matplotlib as mp
import matplotlib.pyplot as plt

from collections import Counter

c_dict = None

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, "w")
    sys.stderr = open(os.devnull, "w")

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

"""
analyze
@param folder: java project folder
return void
"""

# https://github.com/musiKk/plyj/blob/c27d159b2fffe241a2d091e1be3d79790b216732/example/symbols_visitor.py
class MyVisitor(m.Visitor):
    def __init__(self):
        super(MyVisitor, self).__init__()
        self.first_field = True
        self.first_method = True
        self.methods = []

    def visit_MethodDeclaration(self, method_decl):
        self.methods.append(method_decl)
        return True


class CodeSniffer:
    def __init__(self, folder):
        self.folder = folder
        # self.files = [x for x in os.listdir(folder) if "java" in x]
        self.files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(folder) for f in filenames if os.path.splitext(f)[1] == '.java']
        # print("Found " + str(len(self.files)) + " java files")
        self.trees = {} #dict of file parse trees (indexed by filename)

        if not self.files:
            print("Error: No Java files found in " + str(folder))
            return

        # print("Parsing files...")
        blockPrint()
        for java_file in self.files:
            # java_file = os.path.join(folder, file)
            p = plyj.parser.Parser()
            self.trees[java_file] = p.parse_file(java_file)

        enablePrint()

    def __str__(self):
        return "CodeSniffer: " + str(self.files)


    def output_program_tree(self, test_num):
        OUTFILE = "../visualize/trees/output_tree" + str(test_num) + ".json"
        c_dict = {}
        c_dict["name"] = "Test Project " + str(test_num)
        c_dict["children"] = []
        
        print("Test: " + str(self.folder))
        print(self.files)
        #iterate through all the files in the testfolder
        for k in self.trees:
            tree = self.trees[k]
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



    def long_method_test(self, lim):
        print("Long Method Test (lm=" + str(lim) + ")")
        # print("Excluding comments and whitespace from method line count")
        # print("* Currently If/Else, Inline Declarations treated as one element *")

        for k in self.trees:
            tree = self.trees[k]
            v= MyVisitor()
            tree.accept(v)
            for method in v.methods:
                length = get_method_length(method)
                if (length>lim):
                    print("%s: Method '%s' too long (%d > %d) - recommend reducing len" % (k,method.name, length, lim))

    def long_parameter_test(self, lim):
        print("Long Parameter Test (lp=" + str(lim) + ")")
        
        for k in self.trees:
            tree = self.trees[k]
            v= MyVisitor()
            tree.accept(v)
            for method in v.methods:
                length = get_parameter_length(method)
                if (length>lim):
                    print("%s: Method '%s' parameters too long (%d > %d) - recommend reducing len" % (k,method.name, length, lim))

            
            # print(tree)
            # for t in tree.type_declarations:
            #     if t.__class__.__name__ == "ClassDeclaration":
            #         v = m.Visitor()
            #         tree.accept(v)
            #         print(tree.accept(v))


    # def get_nodes_of_type(self, tree, node_type):
    #     nodes = []

#Need to fix
def get_method_length(method):
    body_elements = method.body
    c = 0
    c = len(body_elements) # NOT CORRECT
    # for node in body_elements:
    #     _name = node.__class__.__name__
    #     if _name == "IfThenElse":
    #         if node.is_true.__class__.__name__ == "Block":
    #             c += len(node.is_true.statements)
    #         else:
    #             c+=1
    #         if node.is_false:
    #             if node.is_false.__class__.__name__ == "Block":
    #                 c += len(node.is_false.statements)
    #             else:
    #                 c+=1

    #     else:
    #         c+=1

    return c


def get_parameter_length(method):
    return len(method.parameters)


def get_node_name(i_name, c_name):
    return i_name + " (" + c_name + ")" 

def get_children(node):   
    temp_obj = {}
    _name = node.__class__.__name__
    
    if _name == "ClassDeclaration":
        temp_obj['name'] = get_node_name(node.name,_name)
        body_elements = getattr(node,"body")
        temp_obj['children'] = [get_children(x) for x in body_elements]
    elif _name == "FieldDeclaration" or _name == "VariableDeclaration":
        temp_obj['name'] = get_node_name(",".join([x.variable.name for x in node.variable_declarators]), _name)
    elif _name == "MethodDeclaration":
        temp_obj['name'] = get_node_name(node.name,_name)
        body_elements = getattr(node,"body")
        temp_obj['children'] = [get_children(x) for x in body_elements]
    # elif _name == "IfThenElse":
    #     temp_obj['name'] = _name
    #     try:
    #         temp_obj['children'] = [{"name": "if_true", "children": get_children(node.if_true.statements)}]
    #         if node.if_false:
    #             temp_obj['children'].append({"name": "if_false", "children": get_children(node.if_false.statements)})
    #     except:
    #         temp_obj['children'] = [{"name": node.if_true.__class__.__name__, "children":[]}]
    else:
        if hasattr(node, "name"):
            temp_obj['name'] = get_node_name(node.name,_name)
        else:
            temp_obj['name'] = _name

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
