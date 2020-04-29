from lxml import etree as ET
from argparse import ArgumentParser
import sys


parser = ArgumentParser(description="Add revision Description to tei files")
parser.add_argument("-s", "--spelling", action="store_true")
parser.add_argument("files", nargs="+")
args = parser.parse_args(sys.argv[1:])

changes = [{"text": "<change>Navigation bars removed</change>", "date": "2020-04-23"},
           {"text": "<change>Paragraphs from original estimated and marked up.</change>", "date": "2020-04-23"},
           {"text": "<change>Seperated sentences using <gi>s</gi> and tokenized using <gi>w</gi> using spaCy.</change>", "date": "2020-04-27"},
           {"text": "<change>POS-Tags added to <att>pos</att> of <gi>w</gi> using spaCy.</change>", "date": "2020-04-27"},
           {"text": "<change>Lemma added to <att>lemma</att> of <gi>w</gi> using spaCy.</change>", "date": "2020-04-27"},
           {"text": "<change>Stop word inidcator added to <att>type</att> of <gi>w</gi> using spaCy.</change>", "date": "2020-04-27"}]
if args.spelling:
    changes.append({"text": "<change>Implicit spelling normalization of manually chosen key terms with manually crafted rules.</change>", "date":"2020-04-24"})
    changes.sort(key= lambda x: x["date"])

ns = {"tei": "http://www.tei-c.org/ns/1.0"}
xml_parser = ET.XMLParser(remove_blank_text=True)
for file in args.files:
    with open(file, "rb") as xml_file:
        tree = ET.parse(xml_file)
    root = tree.getroot()
    teiHeader = root.find(".//tei:teiHeader", ns)
    revDesc = ET.SubElement(teiHeader, "revisionDesc")
    for c in changes:
        c_elem = ET.fromstring(c["text"])
        c_elem.attrib["when"] = c["date"]
        c_elem.attrib["who"] = "Pascal Hein"
        revDesc.append(c_elem)

    outfile = file[:-4] + "_reved.xml"
    ET.indent(root, space="    ")
    tree.write(outfile, encoding="utf-8", method="xml", xml_declaration=True)



