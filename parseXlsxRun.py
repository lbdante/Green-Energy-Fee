# parseXlsxRun runs the xlsx parsing and uses parseXlsx

import parseXlsx as parse
import xlrd
import mysql.connector
import conf
import os


# Opens excel workbook to read from
workbook = xlrd.open_workbook(os.path.join(conf.excel_home, conf.excel_file))
sheet = workbook.sheet_by_name('Refuse')

print parse.generate_statement(sheet, ('A', '1'), 'Test')
