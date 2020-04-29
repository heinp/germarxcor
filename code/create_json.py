from lxml import etree as ET
import sys
from argparse import ArgumentParser
import json
from os import path, makedirs
from collections import defaultdict

parser = ArgumentParser(description="Safe tokens as json")
parser.add_argument("-y", "--filter-symbols", action="store_true")
parser.add_argument("-t", "--filter-stopwords", action="store_true")
parser.add_argument("files", nargs="+")
args = parser.parse_args(sys.argv[1:])

ns = {"tei": "http://www.tei-c.org/ns/1.0"}

addendum = ""
if args.filter_stopwords:
    addendum += "_nosw"
if args.filter_symbols:
    addendum += "_nosy"

# organize files, so that in can be iterated over them in a way that makes saving easy
orged_files = defaultdict(lambda: defaultdict(list))
for file in args.files:
    author = path.basename(path.dirname(path.dirname(file)))
    work = path.basename(path.dirname(file))
    orged_files[author][work].append(file)


print(f"Saving data {len(args.files)} xml-files to {sum(len(w) for w in orged_files.values())} json-files")
c = 0  # counter for the files (because they are iterated over recursively and not in one go
for author, work_files in orged_files.items():
    for work, files in work_files.items():
        # preparing the data structure
        data = defaultdict(list)
        for i, file in enumerate(files):
            print(f"\r{((c+i+1)*100)/len(args.files):05.2f}%", end='')
            print(" transforming...               ", end="")
            # extract metadata information from file path
            doc = path.basename(file)
            work = path.basename(path.dirname(file))
            author = path.basename(path.dirname(path.dirname(file)))
            # read in xml data, use environment because of file handling issues in lxml
            with open(file, "rb") as xml_file:
                tree = ET.parse(xml_file)
            root = tree.getroot()
            sentences = root.findall(".//tei:s", ns)
            # transform every sentence to json and save into data structure
            for sent in sentences:
                new_sent = []
                for token in sent:
                    lemma = token.attrib["lemma"]
                    is_stopword = token.attrib["type"] == "stopword"
                    is_symbol = len(lemma) == 1 and not lemma.isalnum()
                    # save token if there is no active flag rising for an active filter
                    if not (is_stopword and args.filter_stopwords) and not (is_symbol and args.filter_symbols):
                        new_token = f"{lemma.lower()}_{token.attrib['pos'].lower()[0]}"
                        new_sent.append(new_token)
                # save sentence in list form to data structure
                if len(new_sent) > 0:
                    data[doc].append(new_sent)
        c += len(files)
        out_file = f"json/{author}/{work}{addendum}.json"
        path2file = path.dirname(out_file)
        if not path.exists(path2file):
            makedirs(path2file)
        print(f"\033[31D saving to {out_file}...")
        with open(out_file, "w") as of:
            json.dump(data, of, indent=2, ensure_ascii=False)

print("\nDone")


