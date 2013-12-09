# parseXlsxRun runs the xlsx parsing and uses parseXlsx module for additional functions

import parseXlsx as parse
import xlrd
import conf
import os
import mysqlInsert

# Opens excel workbook to read from
workbook = xlrd.open_workbook(os.path.join(conf.excel_home, conf.excel_file))
sheet = workbook.sheet_by_name('Refuse')

# Create a list of building which to pull data for
bldings = ['BI', 'CB', 'PA']

for bld in bldings:
    #Collects statements SQL statements from the excel file
    statements = parse.generate_statements(sheet, bld, '0000/00/00')

    # Inserts all data into database
    mysqlInsert.insert_data(statements)
