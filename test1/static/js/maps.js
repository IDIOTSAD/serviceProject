var map;
var pass;
var lat;
var lon;

  new google.maps.Marker({
    position: seoul,
    map: map,
    label: "서울 중심 좌표"
  });

     function init()
{
    window.navigator.geolocation.getCurrentPosition(current_position);
}

function current_position(position)
{
    var latlng = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);

    lat = position.coords.latitude;
    lon = position.coords.longitude;

    pass = String(position.coords.latitude) + "/" + String(position.coords.longitude);
    document.frm.form_name.value=pass;

    var map_options = {
        center:latlng,zoom:14,
        mapTypeId:google.maps.MapTypeId.ROADMAP,
        mapTypeControl:false,
        navigationControlOptions:{style:google.maps.NavigationControlStyle.SMALL}
    }

    var map = new google.maps.Map(document.getElementById("google_map"), map_options);

    var marker = new google.maps.Marker({position:latlng,map:map,title:"You are here!"});
    }
window.addEventListener("load", init);


function initMap() {
  var seoul = { lat: lat ,lng: lon };
  map = new google.maps.Map( document.getElementById('map'), {
      zoom: 12,
      center: seoul
    });
}