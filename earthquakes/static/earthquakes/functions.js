

function searchEvents() {

var mark=Array();
console.log($('#eventHighMMF').val());
console.log($('#eventLowMMF').val());
console.log($('#eventID').val());
  $.get('/earthquakes/events', {
    "eventID": $('#eventID').val(),
    "eventStartDate": $('#eventStartDate').val(),
    "eventEndDate": $('#eventEndDate').val(),
    "eventStartTime": $('#eventStartTime').val(),
    "eventEndTime": $('#eventEndTime').val(),
    "eventLowMMF": $('#eventLowMMF').val(),
    "eventHighMMF": $('#eventHighMMF').val(),
    "eventLowDepth": $('#eventLowDepth').val(),
    "eventHighDepth": $('#eventHighDepth').val()
  }, function(ret) {

   var json = $.parseJSON(ret);

    $("#results").find("tr:gt(0)").remove();
    var locations= new Array(json.length);
    tr = $('<tr>');
    tr.append("<th>ID</th> <th>DateTime</th> <th>Fi</th><th>Lamda</th><th>Depth</th><th>MMF</th>")
    $('#results').append(tr);
    for (var i = 0; i < json.length; i++) {
      tr = $('<tr/>');
      tr.append("<td>" + json[i].fields.event_id + "</td>");
      tr.append("<td>" + json[i].fields.datetime + "</td>");
      tr.append("<td>" + json[i].fields.fi + "</td>");
      tr.append("<td>" + json[i].fields.lamda + "</td>");
      tr.append("<td>" + json[i].fields.depth + "</td>");
      tr.append("<td>" + json[i].fields.mmf + "</td>");
      $('#results').append(tr);


      var marker = new google.maps.Marker({
        position: myLatlng,
        title: "Hello World!"
      });
    }

    // To add the marker to the map, call setMap();

    return ret; //you can handle with return value ret here
  });


}

function clearStation(){
  $('#stationName').val("");
  $('#stationCode').val("");
  $('#stationFi').val("");
  $('#stationLamda').val("");
  $('#stationHeight').val("");

}
function searchStation() {
  $.get('/earthquakes/stations', {
    "name": $('#stationName').val(),
    "code": $('#stationCode').val(),
    "fi": $('#stationFi').val(),
    "lamda": $('#stationLamda').val(),
    "height": $('#stationHeight').val()

  }, function(ret) {
    var json = $.parseJSON(ret);
    console.log(json["0"].fields.lamda);

    $("#results").find("tr:gt(0)").remove();
    var locations= new Array(json.length);
    tr = $('<tr>');
    tr.append("<th>Name</th> <th>Code</th> <th>Fi</th><th>Lamda</th><th>Heigh</th>")
    $('#results').append(tr);
    for (var i = 0; i < json.length; i++) {
      tr = $('<tr/>');
      tr.append("<td>" + json[i].fields.station_name + "</td>");
      tr.append("<td>" + json[i].fields.station_code + "</td>");
      tr.append("<td>" + json[i].fields.fi + "</td>");
      tr.append("<td>" + json[i].fields.lamda + "</td>");
      tr.append("<td>" + json[i].fields.height + "</td>");
      $('#results').append(tr);

      var myLatlng = new google.maps.LatLng(json[i].fields.fi,json[i].fields.lamda);
      var mapOptions = {
        zoom: 9,
        center: myLatlng
      }
      var map = new google.maps.Map(document.getElementById("map-canvas-2"), mapOptions);

      var marker = new google.maps.Marker({
        position: myLatlng,
        title: "Hello World!"
      });
    }

    // To add the marker to the map, call setMap();
    marker.setMap(map);

    return ret; //you can handle with return value ret here
  });
}

function clearEvents(){
  $('#eventID').val("");
  $('#eventDate').val("");
  $('#eventTime').val("");
  $('#eventFI').val("");
  $('#eventLamda').val("");
  $('#eventDepth').val("");

  $('#DatePicker').DatePicker({
    flat: true,
    date: '2008-07-31',
    current: '2008-07-31',
    calendars: 1,
    starts: 1
  });

}
