import javalang
import os
import numpy as np
import scipy as sp
import matplotlib as mp
import matplotlib.pyplot as plt

from collections import Counter

def analyze(folder):
    files = [x for x in os.listdir(folder)]
    print("Test: " + str(folder))
    #iterate through all the files in the testfolder
    for file in files:
        print("Analyzing: " + str(file))
        f = open(os.path.join(folder, file), "r")
        text = f.read()
        tree = javalang.parse.parse(text)
        tokens = list(javalang.tokenizer.tokenize(text))
        print(tree.package.name)
        plot_token_types(file, tokens)
        # token_values = [t.value for t in tokens]


def plot_token_types(f, tokens):
    counter = Counter([x.__class__.__name__ for x in tokens]).most_common()
    token_names, token_counts = zip(*counter[::-1])

    # Plot histogram using matplotlib barh().
    indexes = np.arange(len(token_names))
    width = 1
    plt.figure(figsize=(16,9))
    plt.barh(indexes, token_counts, width)
    plt.yticks(indexes + width * 0.5, token_names)
    plt.xlabel("Frequency")

    plt.title(str(f) + " Token Composition")
    plt.grid(True)
    plt.show()


#TODO: Add more functions for the pyreflect module

