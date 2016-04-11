import pyreflect
import os, sys
import json

TEST_DIRECTORY = "./../tests"

def runtest(f):
    pyreflect.analyze(f)

def main():
    test_folders = [os.path.join(TEST_DIRECTORY,x) for x in os.listdir(TEST_DIRECTORY)]
    print("starting tests\n---\n")
    for f in test_folders:
        runtest(f)
        print("-"*10)

    print("---\ndone")

if __name__ == "__main__":
    main()



