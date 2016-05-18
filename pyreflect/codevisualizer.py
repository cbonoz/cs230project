#!/usr/bin/env python3


from smellutil import *

"""
name: codevisualizer.py
Visualization Helper Functions (plots and graphs via python numpy, scipy, matplotlib)
"""

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


# def analyze_javalang(folder):
#     #iterate through all the files in the testfolder
#     files = [x for x in os.listdir(folder)]
#     print("Test: " + str(folder))
#     for file in files:
#         print("Analyzing: " + str(file))
#         f = open(os.path.join(folder, file), "r")
#         text = f.read()
#         tree = javalang.parse.parse(text)
#         # print(tree)
#         tokens = list(javalang.tokenizer.tokenize(text))
#         # print(tree.package.name)
#         # plot_token_types(file, tokens)
#         token_values = [t.value for t in tokens]
#         for t in tokens:
#             print(t)



#TODO: Add more visualization functions for the pyreflect module (for non-command line visualization, add support to the website visualization folder via implementation).



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
