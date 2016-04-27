#!/usr/bin/env python3

"""
Chris Buonocore
module: pyreflect
CS 230 Spring 2016 project
UCLA

"""
from codesniffer import *
import sys, argparse

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('-s', action='store', dest='simple_value',
                        help='Store a simple value')

    parser.add_argument('-lm', action='store', dest='long_method_limit', default=-1,
                        help='Run long method test with optional limit value')

    # parser.add_argument('-lm', action='store_true', dest='long_method_limit',
    #                     help='Run long method test with optional limit value')

    parser.add_argument('-lp', action='store', dest='long_parameter_limit', default=-1,
                        help='Run long parameter test with optional limit value')

    parser.add_argument('-c', action='store_const', dest='constant_value',
                        const='value-to-store',
                        help='Store a constant value')

    parser.add_argument('-f', action='store', default=None,
                        dest='target_folder',
                        help='Target project folder')

    parser.add_argument('-a', action='append', dest='collection',
                        default=[],
                        help='Add repeated values to a list',
                        )

    parser.add_argument('-A', action='append_const', dest='const_collection',
                        const='value-1-to-append',
                        default=[],
                        help='Add different values to list')
    parser.add_argument('-B', action='append_const', dest='const_collection',
                        const='value-2-to-append',
                        help='Add different values to list')

    parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    args = parser.parse_args()
    target_folder = args.target_folder
    lm_limit = int(args.long_method_limit)
    lp_limit = int(args.long_parameter_limit)

    if not target_folder:
        print("Usage: Need -f target folder option")
        return

    code_sniffer = CodeSniffer(target_folder)

    # if hasattr(args, "lm"):
    if lm_limit>0:
        code_sniffer.long_method_test(lm_limit)

    if lp_limit>0:
        code_sniffer.long_parameter_test(lp_limit)

    # print("---\ndone")

if __name__ == "__main__":
    main()

