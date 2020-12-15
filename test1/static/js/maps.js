var map;
var lati;
var long;
var psss;

function init()
{
    console.log("시작함")
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(current_position);
    }
    else {
    console.log("실행 안됨")
    }

}

function current_position(position)
{
    console.log("제대로시작함")
    var latlng = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);

    lati = position.coords.latitude;
    long = position.coords.longitude;

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
  var seoul = { lat: lati ,lng: long };
  map = new google.maps.Map( document.getElementById('map'), {
      zoom: 12,
      center: seoul
    });

  new google.maps.Marker({
    position: seoul,
    map: map,
    label: "서울 중심 좌표"
  });
}