$(document).ready(function(){
    $('#accept-friend-request').live("click", function(){
        var id =  $(this).data("note");
        var $parent = $(this).parent();
        $.post('/profile/friendrequest/', {'id': id, 'type': 'accept'}, function(data){
            console.log('nice')
            $('#notifications_bar').html("Friendship accepted!").slideDown(200).delay(1000).slideUp(200);
            $parent.remove();
        });
    });
    
    $('#decline-friend-request').click(function(){
        var id =  $(this).data("note");
        var $parent = $(this).parent();
        $.post('/profile/friendrequest/', {'id': id, 'type': 'decline'}, function(data){
            console.log('nice')
            $('#notifications_bar').html("Friendship rejected!").slideDown(200).delay(1000).slideUp(200);
            $parent.remove();
        });
    });

    $('#accept-clan-request').click(function(){
        var id =  $(this).data("note");
        var $parent = $(this).parent();
        $.post('/alliance/process_request/', {'id': id, 'type': 'accept'}, function(data){
            $('#notifications_bar').html("Clan request accepted!").slideDown(200).delay(1000).slideUp(200);
            $parent.remove();
        });
    });

    $('#decline-clan-request').click(function(){
        var id =  $(this).data("note");
        var $parent = $(this).parent();
        $.post('/alliance/process_request/', {'id': id, 'type': 'decline'}, function(data){
            $('#notifications_bar').html("Clan request refected!").slideDown(200).delay(1000).slideUp(200);
            $parent.remove();
        });
    });

    $('#notification').live('mouseover', function(){

            if ($(this).hasClass('unseen')){
                var id =  $(this).data("note");
                $(this).removeClass('unseen')

                 var notifications_number = parseInt( $('#notifications_nr').html(), 10) - 1


                 $('#notifications_nr').html(notifications_number)
                 $individual_notification = $(this).parents('.notifications_body').prev()

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