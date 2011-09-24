$(document).ready(function(){
    $('#accept-friend-request').live("click", function(){
        var id =  $(this).data("note");
        console.log(id)
        $.post('/profile/friendrequest/', {'id': id, 'type': 'accept'}, function(data){
            console.log('nice')
            //TODO: make succes/fail notification on the client-side
        });
    });
    
    $('#decline-friend-request').click(function(){
        var id =  $(this).data("note");
        $.post('/profile/friendrequest/', {'id': id, 'type': 'decline'}, function(data){
            console.log('nice')
            //TODO: make succes/fail notification on the client-side
        });
    });

    $('#accept-clan-request').click(function(){
        var id =  $(this).data("note");
        $.post('/alliance/process_request/', {'id': id, 'type': 'accept'}, function(data){
            console.log('nice')
            //TODO: make succes/fail notification on the client-side
        });
    });

    $('#decline-clan-request').click(function(){
        var id =  $(this).data("note");
        $.post('/alliance/process_request/', {'id': id, 'type': 'decline'}, function(data){
            console.log('nice')
            //TODO: make succes/fail notification on the client-side
        });
    });

    $('#notification').live('mouseover', function(){

            if ($(this).hasClass('unseen')){
                var id =  $(this).data("note");
                $(this).removeClass('unseen')

                 var notifications_number = parseInt( $('#notifications_nr').html(), 10) - 1


                 $('#notifications_nr').html(notifications_number)
                 $individual_notification = $(this).parents('.notifications_body').prev()
                 console.log($individual_notification)
                 notifications_number = parseInt($individual_notification.html(), 10) - 1
                 if (notifications_number == 0){
                     $individual_notification.css('display', 'none')
                 }else{
                     $individual_notification.html(notifications_number)
                 }

                $.post('/notification/seen/'+id, function(data){
                    console.log('nice')
                    //TODO: send fail/sucesfull notification to frontend
                })
            }
    })

    socket.on('notification', function (data) {
        var notifications_number = parseInt( $('#notifications_nr').html(), 10) + 1
        $('#notifications_nr').html(notifications_number)
        if (data.type == 'friend'){
            
            $('.notifications_items', '#friend_requests').prepend(data.notification)
            notifications_number = parseInt( $('.individual_notifications_bubble', '#friend_requests').html(), 10) + 1
            $('.individual_notifications_bubble', '#friend_requests').html(notifications_number)
            $('.individual_notifications_bubble', '#friend_requests').css('display', 'block')

        }else if(data.type == 'message'){
            
            $('.notifications_items', '#messages').prepend(data.notification)
            notifications_number = parseInt( $('.individual_notifications_bubble', '#messages').html(), 10) + 1
            console.log($('.individual_notifications_bubble', '#messages').html())
            $('.individual_notifications_bubble', '#messages').html(notifications_number)
            $('.individual_notifications_bubble', '#messages').css('display', 'block')

        }else{
            $('.notifications_items', '#alliance_requests').prepend(data.notification)
            notifications_number = parseInt( $('.individual_notifications_bubble', '#alliance_requests').html(), 10) + 1
            $('.individual_notifications_bubble', '#alliance_requests').html(notifications_number)
            $('.individual_notifications_bubble', '#alliance_requests').css('display', 'block')
        }
    });

    
});