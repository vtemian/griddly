$(document).ready(function(){
    $('#territoryVenue').live('click', function(){
        var lat = $(this).data('lat');
        var lng = $(this).data('lng');

        var point = new google.maps.LatLng(lat, lng);
        app.map.setCenter(point, 17);
    });
})