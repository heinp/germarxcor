from lxml import etree as ET
from argparse import ArgumentParser
import sys
from os import path
from collections import defaultdict
import matplotlib.pyplot as plt
import random
import numpy as np


def type_token_ratio(toks, n=None, method="abs"):
    if method == "abs":
        tok_count = len(toks)
        type_count = len(set(toks))
    if method == "samp":
        tok_count = n if n is not None else 50000
        r = 5
        type_counts = [len(set(random.sample(toks, tok_count))) for _ in range(r)]
        type_count = sum(type_counts)/r
    if method == "sttr":
        chunk_size = n if n is not None else 1000
        chunks = len(toks)//1000
        total = 0
        for chunk in range(chunks):
            start = chunk * chunk_size
            end = start + chunk_size
            ttr = type_token_ratio(toks[start:end])
            total += ttr
        return total / chunks
    return type_count / tok_count


parser = ArgumentParser(description="Add revision Description to tei files")
parser.add_argument("-o", "--output-file", nargs="?", default="metrics.csv")
parser.add_argument("files", nargs="+")
args = parser.parse_args(sys.argv[1:])

# organize files, so that in can be iterated over them in a way that makes saving easy
orged_files = defaultdict(lambda: defaultdict(list))
for file in args.files:
    author = path.basename(path.dirname(path.dirname(file)))
    work = path.basename(path.dirname(file))
    orged_files[author][work].append(file)


data = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

ns = {"tei": "http://www.tei-c.org/ns/1.0"}
for author, works in orged_files.items():
    print(f"Working on {author}...")
    tokens = []
    work_bounds = []
    for work, files in works.items():
        work_bounds.append((work, len(tokens)))
        for file in files:
            doc = path.basename(file)
            work = path.basename(path.dirname(file))
            author = path.basename(path.dirname(path.dirname(file)))
            with open(file, "rb") as xml_file:
                tree = ET.parse(xml_file)
            root = tree.getroot()
            words = root.findall(".//tei:w", ns)
            for w in words:
                tokens.append((w.text.lower(), w.attrib["lemma"]))

    for m in ["abs", "samp", "sttr"]:
        ttr = type_token_ratio([t[0] for t in tokens], method=m)
        data[author][m] = ttr

authors = data.keys()
abs_values = [data[a]["abs"] for a in authors]
samp_values = [data[a]["samp"] for a in authors]
sttr_values = [data[a]["sttr"] for a in authors]

x = np.arange(len(authors))  # the label locations
width = 0.27  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width, abs_values, width, label='abs')
rects2 = ax.bar(x, samp_values, width, label='samp')
rects3 = ax.bar(x + width, sttr_values, width, label="sttr")

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('TTR')
ax.set_title('TTR of different authors')
ax.set_xticks(x)
ax.set_xticklabels(authors)
ax.legend()


fig.tight_layout()

plt.show()

