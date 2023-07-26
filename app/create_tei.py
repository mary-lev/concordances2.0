from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom
import re

def create_TEI(text):
    author = f"{text.author.name} {text.author.surname} {text.author.family}"
    title = text.title
    poem = text.body
    date = text.text_date.year

    # Create the root TEI element
    root = Element('TEI')
    root.set('xmlns', 'http://www.tei-c.org/ns/1.0')

    # Create the teiHeader
    teiHeader = SubElement(root, 'teiHeader')
    fileDesc = SubElement(teiHeader, 'fileDesc')

    # Set the title and author
    titleStmt = SubElement(fileDesc, 'titleStmt')
    SubElement(titleStmt, 'title').text = title
    SubElement(titleStmt, 'author').text = author

    # Add the publicationStmt
    publicationStmt = SubElement(fileDesc, 'publicationStmt')
    SubElement(publicationStmt, 'p').text = 'Unpublished'

    # Add the sourceDesc
    sourceDesc = SubElement(fileDesc, 'sourceDesc')
    SubElement(sourceDesc, 'p').text = 'Automatically created from the database.'

    # Create the text body
    text = SubElement(root, 'text')
    body = SubElement(text, 'body')
    div = SubElement(body, 'div')
    div.set('type', 'poem')

    # Split the poem into stanzas and lines and add them to the XML
    stanzas = re.split("\r\n\r\n", poem)
    for stanza in stanzas:
        lines = stanza.split('\n')
        lg = SubElement(div, 'lg', type="stanza")
        for line in lines:
            l = SubElement(lg, 'l')
            l.text = line

    # Add the date
    date_element = SubElement(div, 'date')
    date_element.set('when', str(date))
    date_element.text = str(date)

    # Convert the XML to a string
    xml_string = tostring(root, 'utf-8')

    # Pretty print the XML
    pretty_xml = minidom.parseString(xml_string).toprettyxml(indent='  ')
    return pretty_xml

