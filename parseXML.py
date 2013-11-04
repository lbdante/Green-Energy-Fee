import MySQLdb as mdb
from xml.dom import minidom
import conf
 
def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)
 
 
# Returns an array of dicts.
# Each array element is a row in the database table.
# Each key of the dict is a column of the table.
# "temp" in the dict would map to the "temp" column in the database.
def parse_xml(filename):
    xml_doc = minidom.parse(filename)
   
    # The following 3 lines builds lists based on the tag name in the xml file.
    # "temp_list" holds every set of "<temp>x</temp>" tags found in the file.
    temp_list = xml_doc.getElementsByTagName('temp')
    power_list = xml_doc.getElementsByTagName('power')
    garbage_list = xml_doc.getElementsByTagName('garbage')
    data = []
 
    # Each element of the data variable represents a row in the database table
    for i in range (0, len(power_list)):
        data.append({'temp': getText(temp_list[i].childNodes),
                    'power': getText(power_list[i].childNodes),
                     'garbage': getText(garbage_list[i].childNodes)})
    return data
 
def insert_data(data):
    try:
        # Replace the parameters here for using a different mysql server
        conn = mdb.connect('127.0.0.1', 'gef', 'gefreedy123', 'gef')
        cur = conn.cursor()
        for row in data:
            #Insert each row of the array into the database
            cur.execute("INSERT INTO gef_data (temp, power, garbage) VALUES (%s, %s, %s)", (row['temp'], row['power'], row['garbage']))
        conn.commit()
        conn.close()
    except mdb.Error, e:
        #Print any mysql errors.
        print "Error %d: %s" % (e.args[0],e.args[1])
       
data = parse_xml('data/xml/report.xml')
#insert_data(data)
