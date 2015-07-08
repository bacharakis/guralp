function searchEvents() {
  $.get('/earthquakes/events', {
    "eventID": $('#eventsID').val(),
    "eventDate": $('#eventDate').val(),
    "eventTime": $('#eventTime').val(),
    "eventFI": $('#eventFI').val(),
    "eventLamda": $('#eventLamda').val(),
    "eventHeight": $('#eventHeight').val(),
    "eventDepth": $('#eventDepth').val()

  }, function(ret) {
    var json = $.parseJSON(ret);
  //  console.log(json["0"].fields.lamda);
    console.log(ret);

    $("#results").find("tr:gt(0)").remove();

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
