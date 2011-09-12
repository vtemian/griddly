$(document).ready(function(){
    $('#add-member').click(function(){
        $('#send-invites').modal({
            opacity:80,
            overlayCss: {backgroundColor:"#5b5b5b"},
            minHeight:400,
            minWidth: 600,
        });
        put_users(users, $('#new-recipient'))
        setAutoComplete("new-recipient", "recipients-results", "/profile/get_users?user=");
    });

    $('#requests').submit(function(){
        var username = $('#username').html()
        var name = $('#clan-name').html()
        $.each(users, function(index, user){
           if(user != username){
                $.post('/alliance/request/', {'user':user, 'name':name}, function(data){
                    var obj = jQuery.parseJSON(data);
                    if (obj.finished != 'not')
                        socket.emit('notification', obj);
                    else
                        console.log('There is an unterminated request, dude ;)')
                    //TODO: send this piece of shit to the client
                })
                console.log('Clan request submited')
               //TODO: request submited notification in client-side
           }else{
               console.log("Dude, you can't submit a clan request to yourself!")
               //TODO: error in page notitication
           }
        });
        $.modal.close();
        return false;
    });
    
    $('#avatar-form').live('submit', function(){
        //TODO: ajax file upload
    });

    $('#create-news').click(function(){
        $('#modal-news').modal({
            opacity:80,
            overlayCss: {backgroundColor:"#5b5b5b"},
            minHeight:400,
            minWidth: 600,
        });
    });

    $('#news-form').submit(function(){
        validate($(this), function(data){
            var news = data.news
            $.each(data.users, function(index, user){
                socket.emit('news-stream', {'recipient': user, 'news':news})
                console.log('as')
            })
        })

        $.modal.close()
        return false;
    });

    function vote(type, label, second){
        var id = $('#news-id', label.parent()).val();
        
        $.post('/clan/vote-news', {'id': id, 'type': type}, function(data){
            if(data == 'ok'){
                $('#value', label).html(parseInt($('#value', label).html()) + 1)
                if(second.hasClass('not-ok')){
                    $('#value', second).html(parseInt($('#value', second).html()) - 1)
                    second.attr('class', 'ok')
                }
                label.attr('class', 'not-ok')
            }else{
                console.log('naspa')
            }
        })
    }

    $('#like.ok').live("click", function(){
        vote("like", $(this), $(this).next())
    })
    $('#unlike.ok').live("click", function(){
        vote("unlike", $(this), $(this).prev())
    })

    //check if u can vote
    $.each($('.simple-news'), function(index, element){
        var id = $('#news-id', element).val()
        $.get('/clan/check-like-state', {'id': id}, function(data){
            if(data == 'ok'){
                $('#like', element).attr('class', 'ok');
                $('#unlike', element).attr('class', 'ok');
            }else if(data == 'is-like'){
                $('#like', element).attr('class', 'not-ok');
                $('#unlike', element).attr('class', 'ok');
            }else{
                $('#like', element).attr('class', 'ok');
                $('#unlike', element).attr('class', 'not-ok');
            }
        })
    });

    $('#del-member').live('click', function(){
        //TODO: realtime notification
        var username = $(this).prev().html().trim()
        var $member = $(this).parent()
        $.post('/clan/del-member', {'username': username}, function(data){
           if(data == 'ok'){
               console.log('The member has been removed!')
               $member.remove()
           }else if(data == 'failed-member'){
               console.log("This member doesn't exists")
           }else if(data == 'failed-rights'){
               console.log("You don't have rights to delete a member")
           }else{
                console.log(data)
           }
        });

    });
})