import pyreflect
import os, sys
import json

TEST_DIRECTORY = "./../tests"

def runtest(f,i):
    pyreflect.analyze(f,i)

def main():
    test_folders = [os.path.join(TEST_DIRECTORY,x) for x in os.listdir(TEST_DIRECTORY)]
    print("starting tests\n---\n")
    i=1
    for f in test_folders:
        runtest(f,i)
        print("-"*10)
        i+=1

    print("---\ndone")

if __name__ == "__main__":
    main()



