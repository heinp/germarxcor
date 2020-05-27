import json
import glob
from collections import defaultdict
from os import path

in_files = glob.glob("../json/*/*")
in_files = [file for file in in_files if "pl" not in file]
orged_files = defaultdict(list)
for file in in_files:
    author = path.basename(path.dirname(file))
    orged_files[author].append(file)


for author, files in orged_files.items():
    author_text = ""
    token_count = 0
    sent_count = 0
    for file in files:
        with open(file) as json_file:
            data = json.load(json_file)
        sents = [item for sublist in data.values() for item in sublist]
        text = [item for sublist in sents for item in sublist]
        sent_count += len(sents)
        token_count += len(text)
        text = " ".join(text)
        author_text += text
    print(author, sent_count)
    #with open(f"../txt/{author}.txt", "w") as out_file:
    #    out_file.write(author_text)

