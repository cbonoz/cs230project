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


"""
REFACTOR STRINGS
"""

LONG_PARAMETER = "Replace Parameter with Method or Introduce Parameter Object"
LONG_METHOD = "Decompose or Refactor Method"
GOD_CLASS = "Extract Subclass"
LAZY_CLASS = "Class should be Merged into Another"
DUPLICATE_CODE = "Extract Method or Refactor"
"""
END REFACTOR STRINGS
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

# Disable print
def blockPrint():
    sys.stdout = open(os.devnull, "w")
    sys.stderr = open(os.devnull, "w")

# Restore print
def enablePrint():
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__


def arg_check(f):
    def wrapper(*args, **kw):
        print("args in decorator: " + str(args))
        if args[1]>0:
            return f(*args, **kw)
        else:
            return (lambda: print("Error: duplicate code limit must be greater than 0"))

    return wrapper


# https://github.com/musiKk/plyj/blob/c27d159b2fffe241a2d091e1be3d79790b216732/example/symbols_visitor.py
class MethodVisitor(m.Visitor):
    def __init__(self):
        super(MethodVisitor, self).__init__()
        self.first_field = True
        self.first_method = True
        self.methods = []

    def visit_MethodDeclaration(self, method_decl):
        self.methods.append(method_decl)
        return True

class ClassVisitor(m.Visitor):
    def __init__(self):
        super(ClassVisitor, self).__init__()
        self.first_field = True
        self.first_method = True
        self.classes = []

    def visit_ClassDeclaration(self,class_decl):
        self.classes.append(class_decl)
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
        # print("Java files: " + str(self.trees.keys()))

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



    @arg_check   
    def long_method_test(self, lim):
        print("Long Method Test (lm=" + str(lim) + ")")
        # print("Excluding comments and whitespace from method line count")
        # print("* Currently If/Else, Inline Declarations treated as one element *")

        for k in self.trees:
            tree = self.trees[k]
            v= MethodVisitor()
            tree.accept(v)
            for method in v.methods:
                length = self.__class__.get_method_length(method)
                if (length>lim):
                    print("%s: Method '%s' lines (%d > %d) - %s" % (k,method.name, length, lim, LONG_METHOD))

    @arg_check
    def long_parameter_test(self, lim):
        print("Long Parameter Test (lp=" + str(lim) + ")")
        
        for k in self.trees:
            tree = self.trees[k]
            v= MethodVisitor()
            tree.accept(v)
            for method in v.methods:
                length = self.__class__.get_parameter_length(method)
                if (length>lim):
                    print("%s: Method '%s' parameters (%d > %d) - %s" % (k,method.name, length, lim, LONG_PARAMETER))


    @arg_check
    def lazy_class(self, lim):
        print("Lazy Class Test (lc=" + str(lim) + ")")
        for k in self.trees:
            tree = self.trees[k]
            v= ClassVisitor()
            tree.accept(v)
            cs = v.classes
            len_cs = len(cs)
            for i, c in enumerate(cs):
                length = self.__class__.get_class_length(c)
                if length<=lim:
                    print("%s: Class '%s' lazy (%d <= %d) - %s" % (k,c.name,length,lim, LAZY_CLASS))



    @arg_check
    def duplicate_code(self, lim):
        print("Duplicate Code Test (lp=" + str(lim) + ")")
        for k in self.trees:
            tree = self.trees[k]
            v= MethodVisitor()
            tree.accept(v)
            ms = v.methods
            len_ms = len(ms)
            for i in range(0,len_ms):
                for j in range(i,len_ms):
                    length = self.__class__.method_similarity(ms[i],ms[j])
                    if length>lim:
                        print("%s: Similar Code: %s, %s - %s" % (k, ms[i].name, ms[j].name, DUPLICATE_CODE))

    """
    1. Class uses directly more than a few attributes of other classes.
    Since ATFD measures how many foreign attributes are used by
    the class, it is clear that the higher the ATFD value for a class, the
    higher is the probability that a class is (or is about to become) a
    God Class.
    2. Functional complexity of the class is very high. This is expressed
    using the WMC (Weighted Method Count) metric.
    3. Class cohesion is low. As a God Class performs several distinct
    functionalities involving disjunct sets of attributes, this has a negative
    impact on the class’s cohesion. The threshold indicates that
    in the detected classes less than one-third of the method pairs
    have in common the usage of the same attribute.
    """

  
    def god_class(self):
        print("God Class Test")

        for k in self.trees:
            tree = self.trees[k]
            v= ClassVisitor()
            tree.accept(v)
            cs = v.classes
            len_cs = len(cs)
            for i, c in enumerate(cs):
                self.__class__.check_god_class(c,k)
                    

 
    @staticmethod
    def check_god_class(c,k):
        #weghted method count
        wmc = 0
        #count of foreign method accesses
        atfd = 0
        #measure of method coupling
        tcc = 0


        class_body = c.body
        methods = [x for x in class_body if x.__class__.__name__ == "MethodDeclaration"]

        for m in methods:
            method_body = m.body
            for b in method_body:
                if is_foreign_call(b) or is_foreign_access(b):
                    atfd+=1
                if b.__class__.__name__ in WMC_OBJECTS:
                    wmc += wmc_count(b)

        methodPairs = count_method_pairs(methods)
        totalMethodPairs = len(methods) * (len(methods) - 1) / 2;
        tcc = methodPairs / totalMethodPairs



        if (wmc >= WMC_VERY_HIGH and atfd > FEW_THRESHOLD and tcc > ONE_THIRD_THRESHOLD):
            print("%s: %s God Class (WMC=%d, ATFD=%d, TCC=%d) - %s" % (k, c.name, wmc, atfd, tcc, GOD_CLASS))
        else:
            print("%s: %s not God Class (WMC=%d, ATFD=%d, TCC=%d)" % (k, c.name,wmc, atfd, tcc))


    @staticmethod
    def method_similarity(method1, method2):
        #returns if two methods are sufficiently similar to be refactored
        body1 = method1["body"]
        body2 = method2["body"]
        if abs(len(body1) - len(body2)) > 3:
            return 0 #not similar
        body1 = set([str(x) for x in body1])
        body2 = set([str(x) for x in body2])
        return len(body1.intersection(body2))

    @staticmethod
    def get_parameter_length(method):
        return len(method.parameters)

    @staticmethod
    def get_class_length(c):
        return len(c["body"])

    #Need to fix
    @staticmethod
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


def is_foreign_access(b):
    return True

def is_foreign_call(b):
    return True

def wmc_count(m):
    count = 0

    return count



def count_method_pairs(methods):
    return 0



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
