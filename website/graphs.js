window.onload = function(){
	var svg = dimple.newSvg("#chartContainer", 800, 550),
	data = [
		{ "Consumable":"Natural Gas", "Year": 2013, "Value" : 639},
		{ "Consumable":"Natural Gas", "Year": 2014, "Value" : 922},
		{ "Consumable":"CO2", "Year": 2013, "Value" : 199},
		{ "Consumable":"CO2", "Year": 2014, "Value" : 823},
		{ "Consumable":"Waste", "Year": 2013, "Value" : 999},
		{ "Consumable":"Waste", "Year": 2014, "Value" : 799},
		{ "Consumable":"Water", "Year": 2013, "Value" : 90},
		{ "Consumable":"Water", "Year": 2014, "Value" : 600}
	],
	
	chart = new dimple.chart(svg, data);
	
	chart.assignColor("2013", "#6C6C6C", "#6C6C6C", .75);
	chart.assignColor("2012", "#005794", "#005794", .75);
	
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
	// x.addOrderRule("Consumable");
	
	x.addOrderRule("Year", true);
	
	// No x label because it's obvious
	x.title = null;
	y.title = "KWH used";

	legend = chart.addLegend(0, 30, "100%", 400, "right", s);
	legend.fontSize = "14px"
	
	
	chart.draw();
	

	// Rotate x axis labels (Consumable names) 45 degrees
	//x.shapes.selectAll("text").attr("transform",
	//	function (d) {
	//		return d3.select(this).attr("transform") + " translate(2, 35) rotate(-45)";
	//	});
	}
