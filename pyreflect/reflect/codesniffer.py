#!/usr/bin/env python3

from smellutil import *
# from clint.textui import colored, puts
# 
OUTFILE_BASE = "../website/app/trees/project_"

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


# Disable print
def blockPrint():
    sys.stdout = open(os.devnull, "w")
    sys.stderr = open(os.devnull, "w")

# Restore print
def enablePrint():
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__


# def arg_check(f):
#     def wrapper(*args, **kw):
#         print("args in decorator: " + str(args))
#         if args[1]>0:
#             return f(*args, **kw)
#         else:
#             return (lambda: print("Error: duplicate code limit must be greater than 0"))

#     return wrapper


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
        self.files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(folder) for f in filenames if os.path.splitext(f)[1] == '.java']
        self.trees = {} #dict of file parse trees (indexed by filename)

        if not self.files:
            print("Error: No Java files found in " + str(folder))
            return

        # print("Parsing files...")
        blockPrint() #prevent debug output from parser
        for java_file in self.files:
            # java_file = os.path.join(folder, file)
            p = plyj.parser.Parser()
            self.trees[java_file] = p.parse_file(java_file)

        enablePrint()
        # print("Java files: " + str(self.trees.keys()))

    def __str__(self):
        return "CodeSniffer: " + str(self.files)


    def output_program_tree(self, test_num):
        c_dict = {}
        c_dict["name"] = "Test Project " + str(test_num)
        c_dict["children"] = []
        
        # print("Test: " + str(self.folder))
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
        # out_file = "./project_" + str(test_num) + ".json"
        out_file = OUTFILE_BASE + str(test_num) + ".json"
        f = open(out_file, "w" )
        f.write(json.dumps(c_dict))
        f.close()
        print("Wrote %s tree to %s" % (k, out_file))



    def long_method_test(self, lim):
        print("Long Method Test (lm=" + str(lim) + ")")
        # print("Excluding comments and whitespace from method line count")
        # print("* Currently If/Else, Inline Declarations treated as one element *")

        for k in self.trees:
            tree = self.trees[k]
            v= MethodVisitor()
            tree.accept(v)
            for method in v.methods:
                length = get_method_length(method)
                if (length>lim):
                    print("%s: Method '%s' lines (%d > %d) - %s" % (k,method.name, length, lim, LONG_METHOD))

    def long_parameter_test(self, lim):
        print("Long Parameter Test (lp=" + str(lim) + ")")
        
        for k in self.trees:
            tree = self.trees[k]
            v= MethodVisitor()
            tree.accept(v)
            for method in v.methods:
                length = get_parameter_length(method)
                if (length>lim):
                    print("%s: Method '%s' parameters (%d > %d) - %s" % (k,method.name, length, lim, LONG_PARAMETER))


  
    def lazy_class(self, lim):
        print("Lazy Class Test (lc=" + str(lim) + ")")

        for k in self.trees:
            tree = self.trees[k]
            v= ClassVisitor()
            tree.accept(v)
            cs = v.classes
            len_cs = len(cs)
            for i, c in enumerate(cs):
                length = get_class_length(c)
                if length<=lim:
                    print("%s: Class '%s' lazy (%d <= %d) - %s" % (k,c.name,length,lim, LAZY_CLASS))



    #TODO: currently fails
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
                    length = method_similarity(ms[i],ms[j])
                    if length>lim:
                        print("%s: Similar Code: %s, %s - %s" % (k, ms[i].name, ms[j].name, DUPLICATE_CODE))

  
    def god_class(self):

        print("God Class Test")
        for k in self.trees:
            tree = self.trees[k]
            v= ClassVisitor()
            tree.accept(v)
            cs = v.classes
            len_cs = len(cs)
            for i, c in enumerate(cs):
                check_god_class(c,k)
                    

 
