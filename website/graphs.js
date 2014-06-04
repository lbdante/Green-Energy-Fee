function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}

function fillBuildingTitle(buildingCode) {
    // buildings should be in buildings.js, refactored to make gregs life easy
	if (buildings.hasOwnProperty(buildingCode)) {
		$('#buildingName').text(buildings[buildingCode] + " - Utility Usage");
	}
}

// Given a building code ("OM"), get the JSON representation of waste, etc.
function getBuildingJSON(buildingCode) {
  
	console.log("getBuildingJSON called with " + buildingCode);
	
	if (buildingCode == "" || buildingCode == null) return;

	requestAddress = "http://" + window.location.host +  "/lookup?code=" + buildingCode;

        console.log(requestAddress);
	$.getJSON(requestAddress , function (response) { 
		console.log("AJAX respone recieved");
		jsonData = transformJsonToGraphData(response);
		jsonData = normalizeGraphData(jsonData);		

		makeGraph(jsonData);
	});
}

// Normalizes until I can figure out how to show percentages
function normalizeGraphData(json) {
	var firstIsBigger;
	var bigger;
	var smaller;

	for (i = 0; i < json.length; i += 2) {



		ratio =  json[i].Value / json[i + 1].Value;
		ratioRounded = Math.round(ratio * 100);

        json[i].Value = 100;
        json[i + 1].Value = ratioRounded;

		console.log("ratio: " + ratio);
	}

	return json;
}

// Transform a json object to a graph data object
function transformJsonToGraphData(json) {
	numberOfUtilities = json.utilities.length;
	currentYear = json.currYear;
	previousYear = json.prevYear;

	console.log("Number of utilities is: " + numberOfUtilities);
	console.log("Current year is: " + currentYear);
	console.log("Prev year is: " + previousYear);
	
	data = [];
	
	for (i = 0; i < numberOfUtilities; i++) {
		util = json.utilities[i];

		if (util.currMeasurement == null) continue;

		console.log("Consumable: " + util.type + " Year: " + currentYear + " Value: " + util.currMeasurement);
		data.push({ "Consumable":util.type, "Year":currentYear, "Value": util.currMeasurement});
		data.push({ "Consumable":util.type, "Year":previousYear, "Value": util.prevMeasurement});
	}
	
	console.log(data);
	
	return data;
}

function makeGraph(json) {
	// Change title of page to building name
	var buildingName = json.displayName;
	
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
	chart.width = 750;
	chart.height = 500;	
	
	// Order alphebetically by Consumable
	x.addOrderRule("Year", true);
	
	// No x label because it's obvious
	x.title = null;
	y.title = "Percentage";

	legend = chart.addLegend(500, 20, "100%", 400, "left", s);
	legend.fontSize = "14px"
	
	chart.draw();
}

window.onload = function(){
	//svg = dimple.newSvg("#chartContainer", 800, 550),
	svg = dimple.newSvg("#chart", "100%", "100%");
	
	buildingCode = getParameterByName("building");
	// Request JSON building data
	json = getBuildingJSON(buildingCode);
	
	fillBuildingTitle(buildingCode);
}
