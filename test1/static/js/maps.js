var map;

function initMap() {
  var seoul = { lat: 37.0 ,lng: 128.0016985 };
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