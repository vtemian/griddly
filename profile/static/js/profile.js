$(document).ready(function(){
    $('#change-password').submit(function() {
        validate($(this));
        return false;
    });

    $('form[type=placeholder]').submit(function(){
        validate($(this));
        $.each($('input[type=text]', $(this)), function(){
            $(this).attr('placeholder', $(this).val())
            $(this).val('')
        });
        return false;
    });
    
    $('input[type=text]', 'form[type=placeholder]').blur(function(){
        if($(this).val()!='')
            $(this).parents('form:first').submit()

    });

    $('#add-friend').click(function(){
        $.post(window.location.pathname+'/add_friend/', function(data){
           var obj = jQuery.parseJSON(data);
           socket.emit('notification', obj)
        });
        $(this).after('<li><button id="another-request" class="profile_button">Friend Requested</button></li>')
        $(this).remove()
    });
    
    $('#un-friend').click(function(){
        $.post(window.location.pathname+'/un_friend/', function(){
           alert("You've just unfriened him!")
        });
        //TODO: make realtime changes
    });

    $('#reply-btn').click(function(){
        
        $('#replyModalForm').modal({
			opacity:80,
			overlayCss: {backgroundColor:"#5b5b5b"},
            minHeight:400,
	        minWidth: 600,

		});
        
        var user = $(this).data("sender")

        if (jQuery.inArray(user,users) == -1)
            users.push(user)

        console.log(users)
        
        put_users(users, $('#new-recipient'))
        setAutoComplete("new-recipient", "recipients-results", "/profile/get_users?user=");
    });

    $('#replyForm').submit(function(){
        var message = $('#message').val()
        if (message.trim()  != ''){
            $.each(users, function(index, user){
                $.post('/profile/sendmessage/', {'user':user, 'message':message}, function(data){
                    var obj = jQuery.parseJSON(data);
                    socket.emit('notification', obj);

                })
                console.log('message submited')
            });
            $.modal.close();
        }else
            alert("You can't send an empty message!")
        return false;
    })

    $('#private-message').click(function(){
        $('#div-message').modal({
			opacity:80,
			overlayCss: {backgroundColor:"#5b5b5b"},
            minHeight:400,
	        minWidth: 600,
		});
        
        
        if (jQuery.inArray(user,users) == -1)
            users.push(user)
        put_users(users, $('#new-recipient'))
        setAutoComplete("new-recipient", "recipients-results", "/profile/get_users?user=");
    });
    
    $('#message-form').submit(function(){
        var message = $('#message').val()
        if (message.trim()  != ''){
            $.each(users, function(index, user){
                $.post('/profile/sendmessage/', {'user':user, 'message':message}, function(data){
                    var obj = jQuery.parseJSON(data);
                    socket.emit('notification', obj);

                })
                console.log('message submited')
            });
            $.modal.close();
        }else
            alert("You can't send an empty message!")
        return false;
    })

    $('#dismiss-clan').click(function(){
        $span = $(this)
        $.post('/profile/dismiss-clan',function(){
            $span.prev().remove()
            $span.remove()
            console.log('Dude, you run out of clan!')
            //TODO: make success/fail notification
        })
    })
})