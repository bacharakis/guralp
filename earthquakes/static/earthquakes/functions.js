

function searchEvents() {

var mark=Array();
  $.get('/earthquakes/events', {
    "eventID": $('#eventID').val(),
    "eventStartDate": $('#eventStartDate').val(),
    "eventEndDate": $('#eventEndDate').val(),
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

      mark=[json[i].fields.event_id, json[i].fields.fi, json[i].fields.lamda, i];
      locations[i]=mark;

    }

var map = new google.maps.Map(document.getElementById('map-canvas-2'), {
  zoom: 7,
  center: new google.maps.LatLng(40.6388,22.9482),
  mapTypeId: google.maps.MapTypeId.ROADMAP
});

var infowindow = new google.maps.InfoWindow();

var marker, i;

for (i = 0; i < locations.length; i++) {
  marker = new google.maps.Marker({
    position: new google.maps.LatLng(locations[i][1], locations[i][2]),
    map: map
  });

  google.maps.event.addListener(marker, 'click', (function(marker, i) {
    return function() {
      infowindow.setContent(locations[i][0]);
      infowindow.open(map, marker);
    }
  })(marker, i));
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

      mark=[json[i].fields.event_id, json[i].fields.fi, json[i].fields.lamda, i];
      locations[i]=mark;
    }

    var map = new google.maps.Map(document.getElementById('map-canvas-2'), {
      zoom: 7,
      center: new google.maps.LatLng(40.6388,22.9482),
      mapTypeId: google.maps.MapTypeId.ROADMAP
    });

    var infowindow = new google.maps.InfoWindow();

    var marker, i;

    for (i = 0; i < locations.length; i++) {
      marker = new google.maps.Marker({
        position: new google.maps.LatLng(locations[i][1], locations[i][2]),
        map: map
      });

      google.maps.event.addListener(marker, 'click', (function(marker, i) {
        return function() {
          infowindow.setContent(locations[i][0]);
          infowindow.open(map, marker);
        }
      })(marker, i));
}
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
