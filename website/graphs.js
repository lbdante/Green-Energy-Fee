// Given a building code ("OM"), get the JSON representation of waste, etc.
function getBuildingJSON(buildingCode) {
	// Make AJAX request
	// someurl.cs.wwu.edu/getJsonBuildingData.cgi?buildingCode= + buildingCode;
	var json = {
		"displayName": "Old Main",
		"buildingCode": "OM",
		"currentYear": 2014,
		"previousYear": 2013,
		"utilities": [
		{
		"type": "Natural Gas",
		"unitMeasure": "KWH",
		"currentYearValue": 1351,
		"previousYearValue": 852
		},
		{
		"type": "Electric",
		"unitMeasure": "KWH",
		"currentYearValue": 1025,
		"previousYearValue": 1526
		},
		{
		"type": "Garbage",
		"unitMeasure": "KWH",
		"currentYearValue": 300,
		"previousYearValue": 400
		},
		{
		"type": "Steam",
		"unitMeasure": "Lbs",
		"currentYearValue": 210,
		"previousYearValue": 512
		}
		],
		"currentYearCo2Value": 22563,
		"previousYearCo2Value": 124912515231,
		"co2UnitMeasure": "Lbs"
		};
	
	return json;
}

// Transform a json object to a graph data object
function transformJsonToGraphData(json) {
	numberOfUtilities = json.utilities.length;
	currentYear = json.currentYear;
	previousYear = json.previousYear;
	
	data = [];
	
	for (i = 0; i < numberOfUtilities; i++) {
		util = json.utilities[i];
		data.push({ "Consumable":util.type, "Year":currentYear, "Value": util.currentYearValue});
		data.push({ "Consumable":util.type, "Year":previousYear, "Value": util.previousYearValue});
	}
	
	console.log(data);
	
	return data;
}

window.onload = function(){
	svg = dimple.newSvg("#chartContainer", 800, 550),

	// Request JSON building data
	json = getBuildingJSON(null /*building name eventually*/);	
	data = transformJsonToGraphData(json);
	
	// Change title of page to building name
	var buildingName = json.displayName;
	$('#buildingName').text(buildingName + " - Energy Usage");
	
	chart = new dimple.chart(svg, data);
	
	// TODO: Change "color years" in 2020
	chart.assignColor("2013", "#6C6C6C", "#6C6C6C", .75);
	chart.assignColor("2014", "#005794", "#005794", .75);
	chart.assignColor("2015", "#6C6C6C", "#6C6C6C", .75);
	chart.assignColor("2016", "#005794", "#005794", .75);
	chart.assignColor("2017", "#6C6C6C", "#6C6C6C", .75);
	chart.assignColor("2018", "#005794", "#005794", .75);
	chart.assignColor("2019", "#6C6C6C", "#6C6C6C", .75);
	chart.assignColor("2020", "#005794", "#005794", .75);
	
	// Bind data to axes
	x = chart.addCategoryAxis("x", ["Consumable", "Year"]);
	x.addGroupOrderRule("Year");
	y = chart.addMeasureAxis("y", "Value");
	
	// Make bar chart 
	s = chart.addSeries("Year", dimple.plot.bar);
	
	// Width/height
	chart.width = 700;
	chart.height = 400;
	
	// Order alphebetically by Consumable
	x.addOrderRule("Year", true);
	
	// No x label because it's obvious
	x.title = null;
	y.title = "WHAT SHOULD THIS BE?";

	legend = chart.addLegend(0, 30, "100%", 400, "right", s);
	legend.fontSize = "14px"
	
	chart.draw();
	
	// Rotate x axis labels (Consumable names) 45 degrees
	//x.shapes.selectAll("text").attr("transform",
	//	function (d) {
	//		return d3.select(this).attr("transform") + " translate(2, 35) rotate(-45)";
	//	});
}
