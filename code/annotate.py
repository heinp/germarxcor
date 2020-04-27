from lxml import etree as ET
import sys
from argparse import ArgumentParser
import spacy
from nltk.tokenize import sent_tokenize, word_tokenize
from spelling_dict import sd
import re


# handle bad encoding and outdated writing
def custom_tokenizer(text):
    global args
    naive_toks = word_tokenize(text, language="german")
    toks = []
    traces = [r"Ã¤", r"Ã\x84'", r"Ã¶", r"Ã\x96", r"Ã¼", r"Ã\x9c", r"Ã\x9f"]
    bad_enc = any(c in text for c in traces)
    for tok in naive_toks:
        if bad_enc:
            try:
                new_tok = tok.encode("latin1").decode("utf-8")
            except UnicodeDecodeError:
                new_tok = tok
            except UnicodeEncodeError:
                new_tok = tok

        else:
            new_tok = tok
        hyphens = ["­", "-", "–"]
        if len(new_tok) > 1 and any([h in new_tok for h in hyphens]):
            for h in hyphens:
                new_tok = new_tok.replace(h, "")
        if args.spelling:
            for rule in sd:
                if re.match(rule[0], new_tok):
                    new_tok = rule[1](new_tok)
        parts = re.match(r"([0-9]+)(\w+)", new_tok)
        if parts:
            g = parts.groups()
            new_tok = g[1]
        if new_tok:
            toks.append(new_tok)
    return spacy.tokens.Doc(nlp.vocab, toks)


parser = ArgumentParser(description="Annotate text from tei-file with spacy.")
parser.add_argument("-s", "--spelling", action="store_true", help="correct spelling of some words")
parser.add_argument("files", nargs="+")
args = parser.parse_args(sys.argv[1:])


ns = {"tei": "http://www.tei-c.org/ns/1.0"}
print("Loading language model...")
nlp = spacy.load("de_core_news_md", disable=['parser', 'ner'])
print("Done")
nlp.tokenizer = custom_tokenizer
nlp.add_pipe(nlp.create_pipe('sentencizer'))
print(f"Annotating {len(args.files)} files...")
for i, file in enumerate(args.files):
    print(f"\r{((i+1)*100)/len(args.files):.2f}%", end='')
    xml_parser = ET.XMLParser(remove_blank_text=True)
    with open(file, "rb") as xml_file:
        tree = ET.parse(xml_file, xml_parser)
    root = tree.getroot()
    paras = root.findall(".//tei:p", ns)
    for para in paras:
        text = para.text
        if not text:
            continue
        annotated_tokens = nlp(text)
        para.text = ""
        for sent in annotated_tokens.sents:
            s = ET.SubElement(para, "s")
            for tok in sent:
                w = ET.SubElement(s, "w")
                w.text = tok.text
                w.attrib["pos"] = tok.pos_
                w.attrib["lemma"] = tok.lemma_
                w.attrib["type"] = "stopword" if tok.is_stop else "no_stopword"

    outfile = file[:-4] + "_annotated.xml"
    ET.indent(root, space="    ")
    tree.write(outfile, encoding="utf-8", method="xml", xml_declaration=True)#, pretty_print=True)

print("\r100.00%\nDone")
