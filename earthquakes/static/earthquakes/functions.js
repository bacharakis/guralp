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
function plot(ret){

  var json_items = JSON.stringify($("#rightValues").val())
  $.each($("#rightValues").val(), function(i, obj) {
      window.open("chart.html?id="+obj);
  });

  //  console.log(json_items);


}

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
