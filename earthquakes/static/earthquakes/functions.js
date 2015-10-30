var markersArray = [];

function initialize(a,f){

if(a && f){
  map = new google.maps.Map(document.getElementById('map-canvas-2'), {
   zoom: 7,
   center: new google.maps.LatLng(a,f),
   mapTypeId: google.maps.MapTypeId.ROADMAP
 });

}else{
  map = new google.maps.Map(document.getElementById('map-canvas-2'), {
   zoom: 7,
   center: new google.maps.LatLng(40.6388,22.9482),
   mapTypeId: google.maps.MapTypeId.ROADMAP
 });
}
}
function get_image(){

console.log("sss d q");
html2canvas(document.body, {
  onrendered: function(canvas) {
    document.body.appendChild(canvas);
  },
  width: 300,
  height: 300
});
console.log("hi");




}
function plot_graph(ret){

  var json_items = JSON.stringify($("#rightValues").val())
  $.each($("#rightValues").val(), function(i, obj) {
      window.open("chart.html?id="+obj);
  });

  //  console.log(json_items);


}
function plot_graph2(ret){


		/* implementation heavily influenced by http://bl.ocks.org/1166403 */
		/* some arguments AGAINST the use of dual-scaled axes line graphs can be found at http://www.perceptualedge.com/articles/visual_business_intelligence/dual-scaled_axes.pdf */

		// define dimensions of graph
		var m = [80, 80, 80, 80]; // margins
		var w = 900 - m[1] - m[3];	// width
		var h = 400 - m[0] - m[2]; // height

		// create a simple data array that we'll plot with a line (this array represents only the Y values, X will just be the index location)
		var data1 = [3, 6, 2, 7, 5, 2, 0, 3, 8, 9, 2, 5, 9, 3, 6, 3, 6, 2, 7, 5, 2, 1, 3, 8, 9, 2, 5, 9, 2, 7];
		var data2 = [543, 367, 215, 56, 65, 62, 87, 156, 287, 398, 523, 685, 652, 674, 639, 619, 589, 558, 605, 574, 564, 496, 525, 476, 432, 458, 421, 387, 375, 368];

		// X scale will fit all values from data[] within pixels 0-w
		var x = d3.scale.linear().domain([0, data1.length]).range([0, w]);
		// Y scale will fit values from 0-10 within pixels h-0 (Note the inverted domain for the y-scale: bigger is up!)
		var y1 = d3.scale.linear().domain([0, 10]).range([h, 0]); // in real world the domain would be dynamically calculated from the data
		var y2 = d3.scale.linear().domain([0, 700]).range([h, 0]);  // in real world the domain would be dynamically calculated from the data
			// automatically determining max range can work something like this
			// var y = d3.scale.linear().domain([0, d3.max(data)]).range([h, 0]);

		// create a line function that can convert data[] into x and y points
		var line1 = d3.svg.line()
			// assign the X function to plot our line as we wish
			.x(function(d,i) {
				// verbose logging to show what's actually being done
				console.log('Plotting X1 value for data point: ' + d + ' using index: ' + i + ' to be at: ' + x(i) + ' using our xScale.');
				// return the X coordinate where we want to plot this datapoint
				return x(i);
			})
			.y(function(d) {
				// verbose logging to show what's actually being done
				console.log('Plotting Y1 value for data point: ' + d + ' to be at: ' + y1(d) + " using our y1Scale.");
				// return the Y coordinate where we want to plot this datapoint
				return y1(d);
			})

		// create a line function that can convert data[] into x and y points
		var line2 = d3.svg.line()
			// assign the X function to plot our line as we wish
			.x(function(d,i) {
				// verbose logging to show what's actually being done
				console.log('Plotting X2 value for data point: ' + d + ' using index: ' + i + ' to be at: ' + x(i) + ' using our xScale.');
				// return the X coordinate where we want to plot this datapoint
				return x(i);
			})
			.y(function(d) {
				// verbose logging to show what's actually being done
				console.log('Plotting Y2 value for data point: ' + d + ' to be at: ' + y2(d) + " using our y2Scale.");
				// return the Y coordinate where we want to plot this datapoint
				return y2(d);
			})


			// Add an SVG element with the desired dimensions and margin.
			var graph = d3.select("#graph").append("svg:svg")
			      .attr("width", w + m[1] + m[3])
			      .attr("height", h + m[0] + m[2])
			    .append("svg:g")
			      .attr("transform", "translate(" + m[3] + "," + m[0] + ")");

			// create yAxis
		    var xAxis = d3.svg.axis().scale(x).tickSize(-h).tickSubdivide(true);
			// Add the x-axis.
			graph.append("svg:g")
			      .attr("class", "x axis")
			      .attr("transform", "translate(0," + h + ")")
			      .call(xAxis);


			// create left yAxis
			var yAxisLeft = d3.svg.axis().scale(y1).ticks(4).orient("left");
			// Add the y-axis to the left
			graph.append("svg:g")
			      .attr("class", "y axis axisLeft")
			      .attr("transform", "translate(-15,0)")
			      .call(yAxisLeft);

	  		// create right yAxis
	  		var yAxisRight = d3.svg.axis().scale(y2).ticks(6).orient("right");
  			// Add the y-axis to the right
  			graph.append("svg:g")
  			      .attr("class", "y axis axisRight")
  			      .attr("transform", "translate(" + (w+15) + ",0)")
  			      .call(yAxisRight);

			// add lines
			// do this AFTER the axes above so that the line is above the tick-lines
  			graph.append("svg:path").attr("d", line1(data1)).attr("class", "data1");
  			graph.append("svg:path").attr("d", line2(data2)).attr("class", "data2");

}


  /*$.get('/earthquakes/get_files', {
    "selected_items": json_items,

  }, function(ret) {


    var json_reply = $.parseJSON(ret);
    console.log(json_reply);

    //var locations = [];
    //$.each(JSONObject.results.bindings, function(i, ret) {
    //    locations.push([obj.place.value, obj.lat.value, obj.long.value, obj.page.value]);
    //});


d3.json("get_files?selected_items=%5B%22ARG1_19971118130739.T.dat%22%5D", function(data) {
  //data=json_reply;
  console.log(data);
   var canvas = d3.select("#graph").append("svg")
        .attr("width", 500)
        .attr("height", 500)
        .attr("border", "black")
        .attr("class", "xAxis")


   var group = canvas.append("g")
        .attr("transform", "translate(100,10)")


   var line = d3.svg.line()
        .x(function(d, i) {
            return d.x;
        })
        .y(function(d, i) {
            return d.y;
        });


   group.selectAll("path")
        .data(data).enter()
        .append("path")
        .attr("d", function(d){ return line(d) })
        .attr("fill", "none")
        .attr("stroke", "green")
        .attr("stroke-width", 3);

        var m = [80, 80, 80, 80]; // margins
		    var w = 500 - m[1] - m[3];	// width
		    var h = 500 - m[0] - m[2]; // height

        var y = d3.scale.linear().domain([0, 100]).range([h, 0]);
        var x = d3.scale.linear().domain([0, 100]).range([0, w]);
        var xAxis = d3.svg.axis().scale(x).tickSize(-h).tickSubdivide(true);
        canvas.append("svg:g")
			      .attr("class", "x axis")
			      .attr("transform", "translate(0," + h + ")")
			      .call(xAxis);


        var yAxisLeft = d3.svg.axis().scale(y).ticks(4).orient("right");
  		// Add the y-axis to the left
    		canvas.append("svg:g")
    		      .attr("class", "y axis axisLeft")
    		      .attr("transform", "translate(-15,0)")
    		      .call(yAxisLeft);

});


} //);
//}
*/
function appendEvents(ret){

  var json = $.parseJSON(ret);

   $("#results").find("tr:gt(0)").remove();
   var locations= new Array(json.length);
   tr = $('<tr>');
   tr.append('<th class="sortable">ID</th> <th class="sortable">DateTime</th> <th>Lat</th><th>Long</th><th>Depth</th><th>MMF</th><th>Files</th>')
   $('#results').append(tr);
   for (var i = 0; i < json.length; i++) {
     tr = $('<tr/>');
     tr.append("<td>" + json[i].fields.event_id + "</td>");
     tr.append("<td>" + json[i].fields.datetime + "</td>");
     tr.append("<td>" + json[i].fields.fi + "</td>");
     tr.append("<td>" + json[i].fields.lamda + "</td>");
     tr.append("<td>" + json[i].fields.depth + "</td>");
     tr.append("<td>" + json[i].fields.mmf + "</td>");
     tr.append("<td><a href=\"#\" onClick=\"goto_plotting('"+json[i].fields.datetime+"')\" class=\"button tiny\">Plot files</a></td>");
     $('#results').append(tr);

     mark=[json[i].fields.event_id, json[i].fields.fi, json[i].fields.lamda, i];
     locations[i]=mark;

   }


 var infowindow = new google.maps.InfoWindow();

 var marker, i;

 for (i = 0; i < locations.length; i++) {
 marker = new google.maps.Marker({
   position: new google.maps.LatLng(locations[i][1], locations[i][2]),
   map: map
 });
 markersArray.push(marker);

 google.maps.event.addListener(marker, 'click', (function(marker, i) {
   return function() {
     infowindow.setContent(locations[i][0]);
     infowindow.open(map, marker);
   }
 })(marker, i));
 }
}

function get_files(datetime){
window.location.href = "plot";
    $.get('/earthquakes/files', {
      "datetime": datetime,

    }, function(ret) {

        var json_reply = $.parseJSON(ret);
        for(var i=0; i<json_reply.length; i++){
          console.log(json_reply[i].file_name);
        }

      return ret; //you can handle with return value ret here
    });
}

function goto_plotting(datetime){
  window.location.href = "plot?datetime="+datetime+"&pr=true&un=true&sp=true";
}

function goto_plotting_station(station_code){
  window.location.href = "plot_station?code="+station_code+"&pr=true&un=true&sp=true";
}

function appendStations(ret){

  var json = $.parseJSON(ret);

  $("#results").find("tr:gt(0)").remove();
  var locations= new Array(json.length);
  tr = $('<tr>');
  tr.append("<th>Name</th> <th>Code</th> <th>Lat</th><th>Long</th><th>Heigh</th><th>Soil Class</th><th>VS30</th><th>Owner</th><th>Station Files</th>")
  $('#results').append(tr);
  for (var i = 0; i < json.length; i++) {
    tr = $('<tr/>');
    tr.append("<td>" + json[i].fields.station_name + "</td>");
    tr.append("<td>" + json[i].fields.station_code + "</td>");
    tr.append("<td>" + json[i].fields.fi + "</td>");
    tr.append("<td>" + json[i].fields.lamda + "</td>");
    tr.append("<td>" + json[i].fields.height + "</td>");
    tr.append("<td>" + json[i].fields.soil_class + "</td>");
    tr.append("<td>" + json[i].fields.vs30 + "</td>");
    tr.append("<td>" + json[i].fields.owner + "</td>");
    tr.append("<td><a href=\"#\" onClick=\"goto_plotting_station('"+json[i].fields.station_code+"')\" class=\"button tiny\">Plot station files</a></td>");
    $('#results').append(tr);

    mark=[json[i].fields.station_name, json[i].fields.station_code, json[i].fields.fi, json[i].fields.lamda, i];
    locations[i]=mark;
  }




  var infowindow = new google.maps.InfoWindow();

  var marker, i;

  for (i = 0; i < locations.length; i++) {

    marker = new google.maps.Marker({
      position: new google.maps.LatLng(locations[i][2], locations[i][3]),
      map: map
    });
    markersArray.push(marker);

    google.maps.event.addListener(marker, 'click', (function(marker, i) {
      return function() {
        infowindow.setContent(locations[i][1]+" "+locations[i][0]);
        infowindow.open(map, marker);
      }
    })(marker, i));
}

}
function searchEvents() {

var mark=Array();
  $.get('/earthquakes/events', {
    "eventID": $('#eventID').val(),
    "eventStartDate": $('#eventStartDate').val(),
    "eventEndDate": $('#eventEndDate').val(),
    "eventLowMMF": $('#eventLowMMF').val(),
    "eventHighMMF": $('#eventHighMMF').val(),
    "eventLowDepth": $('#eventLowDepth').val(),
    "eventHighDepth": $('#eventHighDepth').val(),
    "A": map.getCenter().lat(),
    "F": map.getCenter().lng(),
    "zoom": map.getZoom(),
    "includeMap" : $('#includeMap').prop("checked"),

  }, function(ret) {

clearMarkers();

appendEvents(ret);
    return ret; //you can handle with return value ret here
  });


}

function clearStation(){
  $('#stationName').val("");
  $('#stationCode').val("");
  $('#stationVs30High').val("");
  $('#stationVs30Low').val("");
  $('#stationHeight').val("");
  $('#stationOwner').val("");
  $('#stationSoilClass').val("");

}
function clearMarkers(){


  for (var i = 0; i < markersArray.length; i++ ) {
    markersArray[i].setMap(null);
  }
  markersArray.length = 0;


}

function searchStation() {
  $.get('/earthquakes/stations', {
    "name": $('#stationName').val(),
    "code": $('#stationCode').val(),
    "height": $('#stationHeight').val(),
    "soilClass": $('#stationSoilClass').val(),
    "vs30High": $('#stationVs30High').val(),
    "vs30Low": $('#stationVs30Low').val(),
    "owner": $('#stationOwner').val(),
    "A": map.getCenter().lat(),
    "F": map.getCenter().lng(),
    "zoom" : map.getZoom(),
    "includeMap" : $('#includeMap').prop("checked"),

  }, function(ret) {
      clearMarkers();
      appendStations(ret);
    return ret; //you can handle with return value ret here
  });
}

function clearEvents(){
  $('#eventID').val("");
  $('#eventStartDate').val("");
  $('#eventEndDate').val("");
  $('#eventLowMMF').val("");
  $('#eventHighMMF').val("");
  $('#eventHighDepth').val("");
  $('#eventLowDepth').val("");

}

function refresh_station_files(station_code){
$("#rightValues option").remove();
$("#leftValues option").remove();
pr=$('#processed').prop("checked");
un=$('#unprocessed').prop("checked");
sp=$('#spectra').prop("checked");
window.location.href = "plot_station?code="+station_code+"&pr="+pr+"&un="+un+"&sp="+sp;

}
function refresh_files(datetime){
$("#rightValues option").remove();
$("#leftValues option").remove();
pr=$('#processed').prop("checked");
un=$('#unprocessed').prop("checked");
sp=$('#spectra').prop("checked");
window.location.href = "plot?datetime="+datetime+"&pr="+pr+"&un="+un+"&sp="+sp;

}

function btnRight() {
    var selectedItem = $("#leftValues option:selected");
    $("#rightValues").append(selectedItem);
}


function btnLeft() {
    var selectedItem = $("#rightValues option:selected");
    $("#leftValues").append(selectedItem);
}
function load(){

$('#processed').prop('checked', true);
$('#unprocessed').prop('checked', true);
$('#spectra').prop('checked', true);

$('#download_files').click(function(e) {
    e.preventDefault();  //stop the browser from following
    window.location.href = 'download';
});
}
