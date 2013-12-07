from mysqlInsert import *
from xml.dom import minidom
from datetime import date


filename = 'Energy Cost Report.xml'
path = 'data/xml/'

# This function collects the meaningful tags we will be parsing by the name of the tag.
# SingleMeterList_ListControl contains electric data
# Detail contains more electric data
# table4_Group2 contains all of the steam data
def get_tags(xml_doc):
    tag_list = {}
    tag_list['SingleMeter'] = xml_doc.getElementsByTagName('SingleMeterList_ListControl')
    tag_list['Detail'] = xml_doc.getElementsByTagName('Detail')
    tag_list['table4_Group2'] = xml_doc.getElementsByTagName('table4_Group2')
    return tag_list

def get_electric_data(tag_list):
    electric = {}
    for tag in tag_list['SingleMeter']:
        # Extract key/value pairs from our tag eg <SingleMeter key1="value1" key2="value2">
        # Only some key/value pairs are used
        keys = tag.attributes.keys()
        source_key = keys[6]
        total_cost_key = keys[2]
        electric['source'] = tag.attributes[source_key].value.split('_')[0]
        electric['total_cost'] = tag.attributes[total_cost_key].value
    # Extract key/value pairs from Detail tag. There are 2 Detail tags we're using.
    keys = tag_list['Detail'][0].attributes.keys()
    cost_key = keys[2]
    type_key = keys[0]
    # Second Detail tag
    keys = tag_list['Detail'][1].attributes.keys()
    units_total_key = keys[0]
    electric['type'] = tag_list['Detail'][0].attributes[type_key].value
    electric['cost'] = tag_list['Detail'][0].attributes[cost_key].value
    electric['units_total'] = tag_list['Detail'][1].attributes[units_total_key].value
    # Date is not included in XML file, we have to generate.
    electric['date'] = date.today().isoformat()
    return electric

def get_steam_data(tag_list):
    steam = {}
    for tag in tag_list['table4_Group2']:
        # Extract key/value pairs from our tag eg <table4_Group2 key1="value1" key2="value2">
        # Only some key/value pairs are used
        keys = tag.attributes.keys()
        source_key = keys[0]
        type_key = keys[2]
        units_total_key = keys[4]
        cost_key = keys[3]
        steam['source'] = tag.attributes[source_key].value
        steam['type'] = tag.attributes[type_key].value
        steam['units_total'] = tag.attributes[units_total_key].value
        steam['cost'] = tag.attributes[cost_key].value
        steam['total_cost'] = float(steam['cost']) * int(steam['units_total'])
        steam['date'] = date.today().isoformat()
    return steam

def iter_tags(tag_list):
    # Build an array of data for insertion.
    # Data[0] contains electric data
    # Data[1] contains steam data
    data = []
    data.append(get_electric_data(tag_list))
    data.append(get_steam_data(tag_list))
    return data

# Dispatcher function, handles everything except for inserting data into the database.
def parse_xml(filename):
    xml_doc = minidom.parse(filename)
    tag_list = get_tags(xml_doc)
    return iter_tags(tag_list)
   

data = parse_xml(path+filename)

# Function imported from mysqlInsert.py
insert_data(data)


