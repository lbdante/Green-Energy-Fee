import MySQLdb as mdb
from xml.dom import minidom
import conf

def get_header_info(xml_doc):
    header = {}
    tag = xml_doc.getElementsByTagName('Report')
    header['name'] = tag[0].attributes['Name'].value
    header['sources'] = tag[0].attributes['textbox3'].value
    header['total'] = tag[0].attributes['textbox14'].value
    return header

def print_header_info(header):
    print "Name: " + header['name'] + "\nSources: " + header['sources'] + "\nTotal: " + header['total'] + "\n"

def get_tags(xml_doc):
    tag_list = {}
    tag_list['SingleMeter'] = xml_doc.getElementsByTagName('SingleMeterList_ListControl')
    tag_list['Detail'] = xml_doc.getElementsByTagName('Detail')
    tag_list['table4_Group2'] = xml_doc.getElementsByTagName('table4_Group2')
    return tag_list

def get_electric_data(tag_list):
    electric = {}
    for tag in tag_list['SingleMeter']:
        keys = tag.attributes.keys()
        source_key = keys[6]
        total_cost_key = keys[2]
        electric['source'] = tag.attributes[source_key].value.split('_')[0]
        electric['total_cost'] = tag.attributes[total_cost_key].value
    keys = tag_list['Detail'][0].attributes.keys()
    cost_key = keys[2]
    type_key = keys[0]
    keys = tag_list['Detail'][1].attributes.keys()
    units_total_key = keys[0]
    electric['type'] = tag_list['Detail'][0].attributes[type_key].value
    electric['cost'] = tag_list['Detail'][0].attributes[cost_key].value
    electric['units_total'] = tag_list['Detail'][1].attributes[units_total_key].value
    return electric

def get_steam_data(tag_list):
    steam = {}
    for tag in tag_list['table4_Group2']:
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
    return steam

def iter_tags(tag_list):
    data = []
    data.append(get_electric_data(tag_list))
    data.append(get_steam_data(tag_list))
    return data

def insert_data(data):
    try:
        # Replace the parameters here for using a different mysql server
        conn = mdb.connect(host=conf.server, user=conf.writer_username, passwd=conf.writer_password, db=conf.db)
        cur = conn.cursor()
        for row in data:
            #Insert each row of the array into the database
            cur.execute("INSERT INTO gef (source, type, cost, units_total, total_cost) VALUES (%s, %s, %s, %s, %s)", (row['source'], row['type'], row['cost'], row['units_total'], row['total_cost']))
        conn.commit()
        conn.close()
    except mdb.Error, e:
        #Print any mysql errors.
        print "Error %d: %s" % (e.args[0],e.args[1])
        
        
        
def parse_xml(filename):
    xml_doc = minidom.parse(filename)
    header = get_header_info(xml_doc)
    print_header_info(header)
    tag_list = get_tags(xml_doc)
    return iter_tags(tag_list)
   

data = parse_xml('data/xml/Energy Cost Report.xml')
insert_data(data)

