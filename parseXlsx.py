# parseXlsx.py parses a xlsx file at a given location for information
# in the rows and inserts them into the databse at the url provided

import math

# Defines alphabet
# DONE!
def in_alpha(char):
    return char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# Searches the excel sheet for the abbreviated building name
# and retursn the xlrd coordinates - returns None if none exist
# DONE!
def get_start_coords(excel_sheet, name, last_date):
    for col in range(1, excel_sheet.ncols):
        label = excel_sheet.cell(10, col).value
        if label == name:
            for row in range(19, excel_sheet.nrows):
                if excel_sheet.cell(row, 1).value > last_date:
                    return (row, col)

# Generates a template insert statement for a table insertion
# DONE!
def gen_insert_stmt(table, numcols):
    statement = 'INSERT INTO {}'.format(table)
    statement = statement + ' VALUES ('
    for val in range(numcols - 1):
        statement = statement + '\'{}\', '
    statement = statement + '\'{}\');'
    return statement
    
# Generates a SQL insertion statement to insert data into database
# Todo
def generate_statements(excel_sheet, blding_name, last_date):
    start = get_start_coords(excel_sheet, blding_name, last_date)
    if start == None:
        return ''
    end = (excel_sheet.nrows - 1, start[1])
    queries = []
    for row in range(start[0], end[0]+1):
        # Convert the date entered in excel to SQL date syntax
        date = excel_sheet.cell(row, 1).value
        raw_date = date.split('/')
        date = raw_date[0] + '-' + raw_date[1] + '-' + raw_date[2]
        
        # Read the value of the current cell
        cell = excel_sheet.cell(row, start[1])

        # if the value of the current cell is not empty, generate statement
        if cell.ctype != 0:
            queries.append(gen_insert_stmt('entry', 6).format(
                date,
                4,
                blding_name,
                'hand',
                1.0,
                int(cell.value)
                ))
    return queries

# Gets the name of the building
# Todo - will be added with additional buildings
def get_blding_name(abbrv):
    if abbrv == 'BI':
        return 'Biology Building'
    elif abbrv == 'CB':
        return 'Chemistry Building'
    elif abbrv == 'PA':
        return 'Performing Arts Center'
    else:
        return 'UNDEFINED'
