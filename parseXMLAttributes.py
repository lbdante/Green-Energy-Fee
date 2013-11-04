import MySQLdb as mdb
from xml.dom import minidom
import conf

def get_tags(xml_doc):
    tag_list = {}
    tag_list['singleMeterList'] = xml_doc.getElementsByTagName('SingleMeterList_ListControl')
    tag_list['table1'] = xml_doc.getElementsByTagName('table1')
    tag_list['table2'] = xml_doc.getElementsByTagName('table1')
    tag_list['table6'] = xml_doc.getElementsByTagName('table1')
    tag_list['table7'] = xml_doc.getElementsByTagName('table1')

    return tag_list

def iter_tags(tag_list):
    for tag_list_key, tag in tag_list.iteritems():
        print tag_list_key
        for key in tag[0].attributes.keys():
            print key + ": " + tag[0].attributes[key].value
        print '\n'
        
def parse_xml(filename):
    xml_doc = minidom.parse(filename)
    tag_list = get_tags(xml_doc)
    iter_tags(tag_list)

    
	

 


data = parse_xml('data/xml/report.xml')
print conf.username

