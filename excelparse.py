#!usr/bin/python

#######################
# Author: Allen Suner #
# Date: 05/15/2013    #
#######################

#imports
import xlrd
import json
import argparse
from datetime import date

#python object that will be
#translated into a JSON string
class Building:

	#JSON fields
	name = ""
	code = ""
	currYear = 0
	prevYear = 0
	utilities = None
	currCo2 = 0
	prevCo2 = 0
	co2unit = "" #TODO - ASK GREG Co2 units

	def __init__(self, code):
		self.code = code

		electric = {
			'unit': "kWh",
			'prevMeasurement': None,
			'currMeasurement': None
		}

		steam = {
			'unit': "thm",
			'prevMeasurement': None,
			'currMeasurement': None
		}

		water = {
			'unit': "CCF",
			'prevMeasurement': None,
			'currMeasurement': None
		}

		refuse = {
			'unit': "yds",
			'prevMeasurement': None,
			'currMeasurement': None
		}

		self.co2unit = "lbs"
		self.utilities = [electric, steam, water, refuse]

#main function
def main():
	building, book, code = parse_args()
	buildString(building, book, code)

	JSONString = json.dumps(building.__dict__, indent =4, sort_keys=True)

	print JSONString

#parsing command line arguements
def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("-f", help="filename to be parsed")
	parser.add_argument("-bc", help="two-letter building code")
	args = vars(parser.parse_args())
	filename = args['f']
	code = args['bc']

	building = Building(code)
	book = xlrd.open_workbook(filename)

	#check to see if filename has data
	if (len(book.sheet_names()) == 0):
		raise Exception("File: " + filename + " has no data to read.")
	else:
		return building, book, code

#building a JSON string from the
#two letter building code
def buildString(building, book, code):

	#worksheets
	currElectric = book.sheet_by_name('FY2014 GEFdash Elec kWh')
	prevElectric = book.sheet_by_name('FY2013 GEFdash Elec kWh')
	sheet_electric = {
		0: currElectric,
		1: prevElectric
	}

	currSteam = book.sheet_by_name('FY2014 GEFdash Steam THERMS')
	prevSteam = book.sheet_by_name('FY2013 GEFdash Steam THERMS')
	sheet_steam = {
	 	0: currSteam, 
	 	1: prevSteam
	 }

	currWater = book.sheet_by_name('FY2014 GEFdash Water CCF')
	prevWater = book.sheet_by_name('FY2013 GEFdash Water CCF')
	sheet_water = {
		0: currWater, 
		1: prevWater
	}

	currRefuse = book.sheet_by_name('FY2014 GEFdash Refuse Yds')
	prevRefuse = book.sheet_by_name('FY2013 GEFdash Refuse Yds')
	sheet_refuse = {
		0: currRefuse, 
		1: prevRefuse
	}

	building.currYear = date.today().year
	building.prevYear = building.currYear - 1

	#TODO add sheet_refuse once we figure out how to parse it!
	util_sheets = [sheet_electric, sheet_steam, sheet_water]

	utilCount = -1

	for util in util_sheets:

		utilCount += 1
		sheets = util

		for sh in sheets:
			#find the header
			header_row, building_col = findHeaderRow(sheets[sh], code)
			building_row = findBuildingRow(sheets[sh], code, header_row, building_col)

			mColumn = findMeasurementColumn(sheets[sh], header_row)
			cColumn = findCo2Column(sheets[sh], header_row)

			if sh == 0:
				prevM = getMeasurement(1, sheets, mColumn, building_row)
				utility = building.utilities[utilCount]
				utility['prevMeasurement'] = prevM
				if (utilCount == 0):
					data = getCo2Data(1, sheets, cColumn, building_row)
					building.prevCo2 = data
			else:
				currM = getMeasurement(0, sheets, mColumn, building_row)
				utility = building.utilities[utilCount]
				utility['currMeasurement'] = currM
				if (utilCount == 0):
					data = getCo2Data(0, sheets, cColumn, building_row)
					building.currCo2 = data

			building.name = getBuildingName(sheets[sh], building_row)

#finds header row
def findHeaderRow(sheet, code):
	num_rows = sheet.nrows - 1
	num_cells = sheet.ncols - 1
	header_row = -1
	while header_row < num_rows:
		header_row += 1
		header_cell = -1
		while header_cell < num_cells:
			header_cell += 1
			value = sheet.cell_value(header_row, header_cell)
			value = ' '.join(str(value).split())
			if (value == 'BLDG ID' or value == 'Loc ID'):
				return header_row, header_cell

#find the building row
def findBuildingRow(sheet, code, header_row, building_col):
	#iterate down the BLDG ID Column
	building_row = header_row
	num_rows = sheet.nrows - 1
	while building_row < num_rows:
		building_row += 1
		building_value = sheet.cell_value(building_row, building_col)
		if (building_value == code):
			return building_row

	raise Exception("Building with code: " + code + " does not have data in this file.")

#finds the measurement column
def findMeasurementColumn(sheet, header_row):
	mCol = -1
	num_cells = sheet.ncols - 1
	while mCol < num_cells:
		mCol += 1
		value = sheet.cell_value(header_row, mCol)
		if (str(value).startswith('GraphYTD')):
			return mCol

def findCo2Column(sheet, header_row):
	cCol = -1
	num_cells = sheet.ncols -1
	while cCol < num_cells:
		cCol += 1
		value = sheet.cell_value(header_row, cCol)
		value = ' '.join(str(value).split())
		if (str(value) == 'YTD CO2 SUM'):
			return cCol
	
#gets a measurement
def getMeasurement(year, sheets, mColumn, building_row):
	#BUG BUG - returns a weird float
	measurement = sheets[year].cell_value(building_row, mColumn)
	return int(measurement)

def getCo2Data(year, sheets, cColumn, building_row):
	measurement = sheets[year].cell_value(building_row, cColumn)
	return int(measurement)

#gets the building name on a sheet given an specific row
def getBuildingName(sheet, building_row):
	name = str(sheet.cell_value(building_row, 0))
	name = name.split()
	return name

if __name__=="__main__":
	main()