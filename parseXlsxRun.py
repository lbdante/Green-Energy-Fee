# parseXlsxRun runs the xlsx parsing and uses parseXlsx module for additional functions

import parseXlsx as parse
import xlrd
import mysql.connector
import conf
import os

# Opens excel workbook to read from
workbook = xlrd.open_workbook(os.path.join(conf.excel_home, conf.excel_file))
sheet = workbook.sheet_by_name('Refuse')

# Creates database connection
host, port = conf.db_url.split(':')
db_connection = mysql.connector.connect(user=conf.username,
                                        password=conf.password,
                                        host=host,
                                        port=port,
                                        database=conf.db_name)

# creates cursor handle to interact with the database
db_cursor = db_connection.cursor()

# Create a list of building which to pull data for
bldings = ['BI', 'CB', 'PA']

for bld in bldings:
    # Checks if this is the first time we've entered data for this
    # building into the database
    db_cursor.execute('SELECT COUNT(*) FROM building WHERE abbrv=\'{}\';'.format(
        bld
    ))
    result = db_cursor.fetchone()

    # If we haven't inserted data for this building into the database, insert
    # building entry
    if result[0] == 0:
        db_cursor.execute('INSERT INTO building VALUES (\'{}\', \'{}\');'.format(
            bld, parse.get_blding_name(bld)
        ))

    # Find the last date that has been entered in the database
    db_cursor.execute('SELECT * FROM entry WHERE abbrv=\'{}\' ORDER BY date DESC;'.format(
        bld
        ))
    result = db_cursor.fetchone()

    # If the last entry was found - update result to reflect last date and
    # Skip remaining dates
    # else - just set date to all zeros - guarenteed to be less than any
    # date entered in the file
    if result != None:
        raw_result = str(result[0]).split('-')
        result = raw_result[0] + '/' + raw_result[1] + '/' + raw_result[2]
        while db_cursor.fetchone() != None: None
    else:
        result = '0000/00/00'
    
    # Collects statements SQL statements from the excel file
    statements = parse.generate_statements(sheet, bld, result)

    # Inserts all data into database
    for stmt in statements:
        db_cursor.execute(stmt)

# Close the database connections and commit transactions
db_cursor.close()
db_connection.commit()
db_connection.close()
