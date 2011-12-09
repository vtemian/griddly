$(document).ready(function(){
    $('#warRequest').live('click', function(){
        var username = $(this).data('username');
        var id = $(this).data('id');
        console.log('a');
        $.post('/battle/request/war', {'username': username, 'id': id}, function(data){
            var obj = jQuery.parseJSON(data);
            if(obj.nice != undefined){
                $('#notifications_bar').html("You are in war with "+username).slideDown(200).delay(1000).slideUp(200);
            }else{
                $('#notifications_bar').html(obj.error).slideDown(200).delay(1000).slideUp(200);
            }
        })
    });
});