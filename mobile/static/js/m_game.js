$(document).ready(function(){
    $('alogout').click(function(){
       window.location='/logout/';
    });
    get_locations();
    $('#aRefresh').live('vclick', get_locations);
    $('#aCheckin').live('vclick', function(){
        var nume = $(this).data('name');
        var lat = $(this).data('lat');
        var lng = $(this).data('lng');
        $.get('/external-api/checkin/?username='+username+'&checkin='+nume+'&lng='+lng+'&lat='+lat, function(data){
            if(data=='done'){
                $('#toastOK').toast('show');
            }else if(data=='to short2'){
                $('#toastLate').toast('show');
            }else{
                $('#toastError').toast('show');
            }
        });
    });
});
function get_locations(){
    if (navigator.geolocation) {
           navigator.geolocation.getCurrentPosition(function(position){
               var lat = position.coords.latitude;
               var lng =position.coords.longitude;
               $.get("https://api.foursquare.com/v2/venues/search?ll="+lat+","+lng+"&limit=5&oauth_token=T53KMW3DZTJSK2B0G5BO2F3DVZ0VA0A5KR3PXRIHXS5VCQ5F&v=20111116", function(data){
                   console.log(data.response.venues);
                   var venues = data.response.venues;
                   $('#locationContainer').empty();
                   $.each(venues, function(index, value){
                       var button = '<a id="aCheckin" data-name="'+value.name+'" data-lat="'+value.location.lat+'" data-lng="'+value.location.lng+'" data-role="button" data-theme="c" class="ui-btn ui-btn-corner-all ui-shadow ui-btn-up-c">\
                                        <span class="ui-btn-inner ui-btn-corner-all" aria-hidden="true">\
                                            <span class="ui-btn-text">'+value.name+'</span>\
                                        </span>\
                                    </a>';
                       $('#locationContainer').append(button);
                   });
               });
           }, function(){
               $('#location_test').html("nicer");
           });
      } else {
           $('#location_test').html("Geolocation not supported");
      }
}