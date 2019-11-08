var loc = document.getElementById("location");
var lat,lon;

function getLocation(e) {
  e.preventDefault();
  console.log("Geo");
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
  } else { 
    loc.innerHTML = "Geolocation is not supported by this browser.";
  }
}

function showPosition(position) {
  loc.innerHTML = "Latitude: " + position.coords.latitude + 
  "<br>Longitude: " + position.coords.longitude;
  lat = position.coords.latitude;
  lon = position.coords.longitude; 
}