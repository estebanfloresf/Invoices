import xml.etree.ElementTree as ET
import lxml.etree as et


root = ET.parse('./data/sample1.xml').getroot()
# print(root.tag)


def print_childs():
    for child in root:
        
        if child.tag == 'comprobante':
             r = requests.get('http://www.forexfactory.com/ffcal_week_this.xml')
             data = et.fromstring(r.text.encode("utf-8"))
        


print_childs()