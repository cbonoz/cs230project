import codesniffer
import os, sys
import json

TEST_DIRECTORY = "./../tests/old"#code-smell-examples"

def runtest(f,test_number):
    code_sniffer = codesniffer.CodeSniffer(f)
    code_sniffer.output_program_tree(test_number)

def main():
    test_folders = [os.path.join(TEST_DIRECTORY,x) for x in os.listdir(TEST_DIRECTORY) if os.path.isdir(os.path.join(TEST_DIRECTORY,x))]
    print("starting tests\n---\n")
    test_number=1
    for f in test_folders:
        print("-"*10)
        runtest(f,test_number)
        test_number+=1

    print("---\ndone")

if __name__ == "__main__":
    main()



