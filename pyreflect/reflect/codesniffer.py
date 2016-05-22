#!/usr/bin/env python3

import smellutil as sm
import plyj.parser
import plyj.model as m
import os, json, sys
import sys, argparse, time
# from clint.textui import colored, puts
# 
OUTFILE_BASE = "../website/app/trees/project_"

"""
REFACTOR STRINGS
"""

LONG_PARAMETER = "Recommend: Replace Parameter with Methods or Introduce Parameter Object"
LONG_METHOD = "Recommend: Decompose or Refactor Methods"
GOD_CLASS = "Recommend: Extract Subclasses"
LAZY_CLASS = "Recommend: Classes should be Merged into Another"
DUPLICATE_CODE = "Recommend: Extract Methods or Refactor"

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
    def __init__(self, folder, timed=False, cache_result=False):
        self.folder = folder
        self.files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(folder) for f in filenames if os.path.splitext(f)[1] == '.java']
        self.trees = {} #dict of file parse trees (indexed by filename)
        self.time1 = None
        self.time2 = None
        blockPrint()
        self.p = plyj.parser.Parser()
        enablePrint()

        if not self.files:
            print("Error: No Java files found in " + str(folder))
            return

        # print("Parsing files...")
        # blockPrint() #prevent debug output from parser
        for java_file in self.files:
            # java_file = os.path.join(folder, file)
            if timed:
                self.time1 = time.time()

            #TODO: Implement caching
            blockPrint()
            self.trees[java_file] = self.p.parse_file(java_file)
            enablePrint()

            if timed:
                self.time2 = time.time()
                print('Parsing %s took %0.2fs' %  (java_file, (self.time2-self.time1)*1.0))

            

        # enablePrint()
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
            if tree is None:
                continue
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
        found = 0
        for k in self.trees:
            tree = self.trees[k]
            if tree is None:
                continue
            v = MethodVisitor()
            tree.accept(v)
            for method in v.methods:
                length = sm.get_method_length(method)
                # print(method.name, length)
                if (length>lim):
                    found+=1
                    print("%s: Method '%s' lines (%d > %d)" % (k,method.name, length, lim))

        if found:
            print(str(found) + " violations - " + LONG_METHOD)
        else:
            print("No long methods found")


    def long_parameter_test(self, lim):
        print("Long Parameter Test (lp=" + str(lim) + ")")
        found = 0
        for k in self.trees:
            tree = self.trees[k]
            if tree is None:
                continue
            v = MethodVisitor()
            tree.accept(v)

            for method in v.methods:
                length = sm.get_parameter_length(method)
                # print(method.name, length)
                if (length>lim):
                    found+=1
                    print("%s: Method '%s' parameters (%d > %d)" % (k,method.name, length, lim))


        if found:
            print(str(found) + " violations - " + LONG_PARAMETER)
        else:
            print("No long method parameters found")


  
    def lazy_class(self, lim):
        print("Lazy Class Test (lc=" + str(lim) + ")")
        found = 0
        for k in self.trees:
            tree = self.trees[k]
            v= ClassVisitor()
            tree.accept(v)
            cs = v.classes
            len_cs = len(cs)
            for i, c in enumerate(cs):
                length = sm.get_class_length(c)
                if length<lim:
                    found+=1
                    print("%s: Class '%s' lazy (%d < %d)" % (k,c.name,length,lim))

        if found:
            print(str(found) + " violations - " + LAZY_CLASS)
        else:
            print("No lazy classes found")

    #TODO: currently fails
    def duplicate_code(self, lim):
        print("Duplicate Code Test (lp=" + str(lim) + ")")
        found = 0
        for k in self.trees:
            tree = self.trees[k]
            if tree is None:
                continue
            v= MethodVisitor()
            tree.accept(v)
            ms = v.methods
            len_ms = len(ms)
            for i in range(0,len_ms):
                for j in range(i+1,len_ms):
                    length = sm.method_similarity(ms[i],ms[j])
                    if length>lim:
                        found+=1
                        print("%s: Similar Code in %s/%s (%d > %d)" % (k,  ms[i].name, ms[j].name, length, lim))

        if found:
            print(str(found) + " violations - " + DUPLICATE_CODE)
        else:
            print("No duplicate code cases found")

  
    def god_class(self):

        print("God Class Test")
        found = 0
        for k in self.trees:
            tree = self.trees[k]
            if tree is None:
                continue
            v= ClassVisitor()
            tree.accept(v)
            cs = v.classes
            len_cs = len(cs)
            for i, c in enumerate(cs):
                if (sm.check_god_class(c,k)):
                    found+=1

        if found:
            print(GOD_CLASS)
        else:
            print("No God Classes found")        

 
