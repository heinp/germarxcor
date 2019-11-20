from bs4 import BeautifulSoup as BS
import re
import os
import sys
from lxml import etree

print("Setting up")
input_file = sys.argv[1]
output_file = re.sub("/html/", "/tei/", input_file)
output_file = re.sub(r"\.html?f?", ".xml", output_file)
#output_plain = re.sub("/html/", "/txt/", input_file)
#output_plain = re.sub(r"\.html?f?", ".txt", output_plain)


if not os.path.exists(os.path.dirname(output_file)):
    os.makedirs(os.path.dirname(output_file))
    
#if not os.path.exists(os.path.dirname(output_plain)):
#    os.makedirs(os.path.dirname(output_plain))


with open(input_file) as file:
    html = BS(file.read(), "lxml")   

print("Get meta data")
fulltitle = html.find("title").text
fulltitle = fulltitle.replace("<", "")
fulltitle = fulltitle.replace(">", "")
fulltitle = fulltitle.replace("&", "")
matches = re.match(r"(.*)(: | - )(.*)", fulltitle)


author = "Wladimir Lenin"

if matches is not None:
    title = matches[3]
    #author = matches[1]
else:
    title = fulltitle
dig_source_name = "Marxist Internet Archive"
dig_source_url = "https://www.marxists.org/deutsch/index.htm"
dig_source_licence = "CC-BY-SA-2.0"
dig_source_licence_url = "https://www.marxists.org/admin/legal/cc/by-sa.htm"

print("Extract body")
try:
    text = html.find("body").getText()
except AttributeError:
    text = html.getText()
text = re.sub(r"<(\d{1,4})>", r"", text)
text = text.replace("<", "")
text = text.replace(">", "")
text = text.replace("&", "")


print("Build TEI")
tei = f"""<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:lang="de">
    <teiHeader>
        <fileDesc>
            <titleStmt>
                <title>{title}</title>
                <author>{author}</author>
            </titleStmt>
            <publicationStmt>
                <publisher>Pascal Hein</publisher>
                <idno type="URL">https://www.github.com/heinp/germarxcor</idno>
                <availability>
                    <licence>
                        <ab>CC-BY-SA-4.0</ab>
                        <ref target="https://creativecommons.org/licenses/by/4.0/deed.de">licence</ref>
                    </licence>
                </availability>
            </publicationStmt>
            <sourceDesc>
                <bibl type="digitalSource">
                    <name>{dig_source_name}</name>
                    <idno type="URL">{dig_source_url}</idno>
                    <availability>
                        <licence>
                            <ab>{dig_source_licence}</ab>
                            <ref target="{dig_source_licence_url}">licence</ref>
                        </licence>
                    </availability>
                </bibl>
            </sourceDesc>
        </fileDesc>
    </teiHeader>
    <text>
        <body>
            <p>
                {text}
            </p>
        </body>
    </text>
</TEI>"""



#with open(output_plain, "w") as file:
#    file.write(text)

with open(output_file, "w") as file:
    file.write(tei)

try:
    doc = etree.parse(open(output_file))
except etree.XMLSyntaxError as err:
    print("XML Syntax Error, see error.log")
    with open("error.log", "a") as error_file:
        error_file.write(str(err.error_log))    
print("\n")
