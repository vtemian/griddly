$(document).ready(function(){
    $('#make-clan-form').submit(function(){
        var username = $('#my_username').html()
        var name = $('#clan-name').val()
        console.log('asd')
        validate($(this), function(){
            $.each(users, function(index, user){
               if(user != username){
                   console.log('if state')
                    $.post('/alliance/request/', {'user':user, 'name':name}, function(data){
                        var obj = jQuery.parseJSON(data);
                        socket.emit('notification', obj);
                    })
                    console.log('Clan request submited')
               }else{
                   console.log("Dude, you can't submit a clan request to yourself!")
               }
               window.location = '/clan'
            });
            $.modal.close();
        })
        return false;
    });
});