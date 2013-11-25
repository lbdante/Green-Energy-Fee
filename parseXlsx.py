# parseXlsx.py parses a xlsx file at a given location for information
# in the rows and inserts them into the databse at the url provided

import math

# Defines alphabet
def in_alpha(char):
    return char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# Translates a standard excel-like row,col coordinate
# into a num,num coordinate
# Done!
def translate_from_excel(col, row):
    end_row = int(row)
    end_col = 0
    for index in range(len(col)):
        power = int(math.pow(26, (len(col) - 1) - index))
        end_col = end_col + power * col_to_int(col[index])
    return (end_col - 1, end_row - 1)
    
# Generates a SQL insertion statement to insert data into database
# Todo
def generate_statement(excel_sheet, excel_coords, db_col_name):
    coords = translate_from_excel(*excel_coords)
    return 'NOT DONE YET;'
    
    
# Gets the date of the last entered SQL statement
# Todo
def get_last_date(date):
    print "get_last_date: not implemented yet."

# Converts a alphabetic letter to a int
# Done!
def col_to_int(col):
    if(in_alpha(col)):
        return int(col, base=36) - 9
    else:
        return -1
