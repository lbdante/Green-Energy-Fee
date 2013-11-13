import MySQLdb as mdb
from xml.dom import minidom
#import conf

def get_header_info(xml_doc):
    header = {}
    tag = xml_doc.getElementsByTagName('Report')
    header['name'] = tag[0].attributes['Name'].value
    header['sources'] = tag[0].attributes['textbox3'].value
    header['total'] = tag[0].attributes['textbox14'].value
    return header

def print_header_info(header):
    print "Name: " + header['name'] + "\nSources: " + header['sources'] + "\nTotal: " + header['total']

def get_tags(xml_doc):
    tag_list = {}
    tag_list['SingleMeter'] = xml_doc.getElementsByTagName('SingleMeterList_ListControl')
    return tag_list

def iter_tags(tag_list):
    for tag in tag_list['SingleMeter']:
        keys = tag.attributes.keys()
        source_key = keys[6]
        value_key = keys[2]
        print "Source: " + tag.attributes[source_key].value.split('_')[0]
        print "Value: " + tag.attributes[value_key].value
        
def parse_xml(filename):
    xml_doc = minidom.parse(filename)
    header = get_header_info(xml_doc)
    print_header_info(header)
    tag_list = get_tags(xml_doc)
    iter_tags(tag_list)

data = parse_xml('data/xml/energyCostReport.xml')

