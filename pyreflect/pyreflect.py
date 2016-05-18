#!/usr/bin/env python3

"""
Chris Buonocore
module: pyreflect
CS 230 Spring 2016 project
UCLA

"""
from codesniffer import *
import sys, argparse, time

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('-f', action='store', default=None,
                        dest='target_folder',
                        help='Target project folder',
                        required=True)

    parser.add_argument('-lm', action='store', dest='long_method_limit', default=-1,
                        help='Run long method test with limit value')

    parser.add_argument('-lp', action='store', dest='long_parameter_limit', default=-1,
                        help='Run long parameter test with limit value')

   
    parser.add_argument('-lc', action='store', dest='lazy_class_limit', default=-1,
                        help='Detect Lazy Classes with number of methods/parameters')

    parser.add_argument('-d', action='store', dest='duplicate_code', default=-1,
                        help='Detect duplicate method code with number of similar lines')

    parser.add_argument('-g', action='store_true', dest='god_class', default=False,
                        help='Detect God Classes if present')

    parser.add_argument('-p', action='store_true', dest='program_tree', default=False,
                        help='Build Program Tree for the folder')



    parser.add_argument('-a', action='store_true', default=False,
                        dest='run_all',
                        help='Run all smell tests with defaults')

    parser.add_argument('-t', action='store_true', default=False,
                        dest='timing',
                        help='Run pyreflect with performance timing')

    parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    args = parser.parse_args()
    target_folder = args.target_folder

    lm_limit = int(args.long_method_limit)
    lp_limit = int(args.long_parameter_limit)
    lc_limit = int(args.lazy_class_limit)
    dup_limit = int(args.duplicate_code)
    god_class = bool(args.god_class)
    prog_tree = bool(args.program_tree)

    run_all = bool(args.run_all)

    if not target_folder:
        print("Usage: Need -f target folder option")
        return

    
    if args.timing:
        time1 = time.time()


    #only load the parse tree once
    code_sniffer = CodeSniffer(target_folder)

    if args.timing:
        time2 = time.time()
        

    if run_all:
        #run all tests with default values
        code_sniffer.long_method_test(10)
        code_sniffer.long_parameter_test(3)
        code_sniffer.duplicate_code(5)
        code_sniffer.lazy_class(2)
        code_sniffer.god_class()
    else:
        #run individual tests
        if lm_limit>0:
            code_sniffer.long_method_test(lm_limit)

        if lp_limit>0:
            code_sniffer.long_parameter_test(lp_limit)

        if lc_limit>0:
            code_sniffer.lazy_class(lc_limit)

        if dup_limit>0:
            code_sniffer.duplicate_code(dup_code)

        if god_class:
            code_sniffer.god_class()

        if prog_tree:
            code_sniffer.output_program_tree(1)
 
    # print("---\ndone")
    if args.timing:
        time3 = time.time()
        print('Java Parsing took %0.2fs' %  ((time2-time1)*1.0))
        print('Pyreflect Analysis took %0.2fs' %  ((time3-time2)*1.0))

if __name__ == "__main__":
    main()


