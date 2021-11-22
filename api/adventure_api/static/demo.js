function makeMap(center) {
    var TILE_URL = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
    var MB_ATTR = 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
    mymap = L.map('llmap').setView(center, 13);
    L.tileLayer(TILE_URL, {attribution: MB_ATTR}).addTo(mymap);
}

var layer = L.layerGroup();

function renderCircles(coords) {
   var circles = coords.map(function(arr) {
       return L.circle(arr,1,{color:"red"});
   });
   mymap.removeLayer(layer);
   layer = L.layerGroup(circles);
   mymap.addLayer(layer);
}

