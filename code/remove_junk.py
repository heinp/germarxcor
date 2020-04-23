#! /usr/bin/python3
import sys
from argparse import ArgumentParser
# from xml.etree import ElementTree as ET
from lxml import etree as ET
import html
from xml.dom import minidom


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def remove(f, l, text):
    """Remove the first f and last l lines from string. Also remove unwanted linebreaks."""
    raw_lines = text.split("\n")
    lines = []
    # remove all unwanted empty lines.
    for line in raw_lines:
        if line == "" or line.isspace():
            if len(lines) == 0 or lines[-1][-1] == "\n":  # if there is already one linebreak, do nothing
                continue
            else:
                lines[-1] += "\n"
        else:
            lines.append(line.strip() + " ")
    # check for validity of parameters
    if len(lines) < (f+l+1):
        raise ValueError(f"Text in file {file} shorter than f+l")
    if f < 0 or l < 0:
        raise ValueError("Line parameters must be positive")

    # create the new text bits
    first_lines = ("".join(lines[:f])).strip()
    new_text = ("".join(lines[f:len(lines)-l])).strip()
    last_lines = ("".join(lines[len(lines)-l:])).strip()
    return html.unescape(new_text), first_lines, last_lines


parser = ArgumentParser(description="Delete the first f and the last l lines of body of a given tei file.")
parser.add_argument("-f", "--first", type=int, default=0)
parser.add_argument("-l", "--last", type=int, default=0)
parser.add_argument("-t", "--test", action="store_true", help="Prints result instead of overwriting file.")
parser.add_argument("files", nargs="+")
args = parser.parse_args(sys.argv[1:])

ns = {"tei": "http://www.tei-c.org/ns/1.0"}


for file in args.files:
    xml_parser = ET.XMLParser(remove_blank_text=True)
    tree = ET.parse(file, xml_parser)
    root = tree.getroot()
    para = root.find(".//tei:p", ns)
    text = para.text
    new_text, firsts, lasts = remove(args.first, args.last, text)
    if args.test:
        print(f"""
{bcolors.BOLD}{bcolors.OKGREEN}### File: '{file}'{bcolors.ENDC}
{bcolors.OKBLUE}### First {args.first} lines:{bcolors.ENDC}
{firsts}

{bcolors.OKBLUE}### Last {args.last} lines:{bcolors.ENDC}
{lasts}

{bcolors.OKBLUE}### Text:{bcolors.ENDC}
{new_text[:500]}\n[…]\n{new_text[-500:]}\n""")

    else:
        body = tree.find(".//tei:body", ns)
        body.remove(para)

        text_paragraphs = new_text.split("\n")
        for text_p in text_paragraphs:
            text_p = text_p.strip()
            if text_p != "Anfang der Seite":
                new_para = ET.SubElement(body, "p")
                new_para.text = text_p

        outfile = file[:-4] + "_clean.xml"
        tree.write(outfile, encoding="utf-8", method="xml", xml_declaration=True, pretty_print=True)
