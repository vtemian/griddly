$(document).ready(function(){
    $('#make-clan-form').submit(function(){
        var username = $('#my_username').html()
        var name = $('#clan-name').val()
        validate($(this), function(){
            $.each(users, function(index, user){
               if(user != username){
                    $.post('/alliance/request/', {'user':user, 'name':name}, function(data){
                        var obj = jQuery.parseJSON(data);
                        socket.emit('notification', obj);
                    });
                   $('#notifications_bar').html("Clan request submited").slideDown(200).delay(1000).slideUp(200);
               }else{
                   $('#notifications_bar').html("You can't submit a clan request to yourself!").slideDown(200).delay(1000).slideUp(200);
               }

            });
            window.location = '/clan';
            $.modal.close();
        });
        return false;
    });
});