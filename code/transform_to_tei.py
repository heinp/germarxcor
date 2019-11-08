
# coding: utf-8

# In[2]:


from bs4 import BeautifulSoup as BS
import re
import os
import sys


# In[12]:


input_file = sys.argv[1]
output_file = sys.argv[2]
if not os.path.exists(os.path.dirname(output_file)):
    os.makedirs(os.path.dirname(output_file))


# In[14]:


with open(input_file) as file:
    html = BS(file.read(), "html.parser")   


# In[34]:


fulltitle = html.find("title")
matches = re.match(r"(.*)(: | - )(.*)", fulltitle.text)
if matches is not None:
    title = matches[3]
    author = matches[1]
else:
    author = "Karl Marx, Friedrich Engels"
    title = fulltitle
dig_source_name = "Stimmen der proletarischen Revolution"
dig_source_url = "http://www.mlwerke.de"
dig_source_licence = "N/A"
dig_source_licence_url = "http://mlwerke.de/ies/kontakt.htm"
try:
    text = html.find("body").getText()
except AttributeError:
    text = html.getText()
text = re.sub(r"<(\d{1,4})>", r"[\1]", text) 


# In[39]:


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
                        <ab>CC-BY-4.0</ab>
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


# In[41]:


with open(output_file, "w") as file:
    file.write(tei)

