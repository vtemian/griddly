var delete_token = 0;
$(document).ready(function(){
    $('#add-member').click(function(){
        $('#send-invites').modal({
            opacity:80,
            overlayCss: {backgroundColor:"#5b5b5b"},
            minHeight:400,
            minWidth: 300
        });
        put_users(users, $('#new-recipient'))
        setAutoComplete("new-recipient", "recipients-results", "/profile/get_users?user=");
    });

    $('#requests').submit(function(){
        var k = 0;
        var username = $('#username').html();
        var name = $('#clan-name').html();
        $.each(users, function(index, user){
           if(user != username){
                $.post('/alliance/request/', {'user':user, 'name':name}, function(data){
                    var obj = jQuery.parseJSON(data);
                    if (obj.finished != 'not')
                        socket.emit('notification', obj);
                    else
                       $('#notifications_bar').html('There is an unterminated request').slideDown(200).delay(1000).slideUp(200);
                });

           }else{
                $('#notifications_bar').html("Dude, you can't submit a clan request to yourself!").slideDown(200).delay(1000).slideUp(200);
                k++;
           }

        });
        if(!k && users.length != 1){
                $('#notifications_bar').html('Clan request submited').slideDown(200).delay(1000).slideUp(200);
        }
        $.modal.close();
        return false;
    });

    $('#member-li', '#member_list').click(function(){
        console.log('a')
        if(delete_token){
            var username = $(this).data('username');
            var $li = $(this);
            $.post('clan/del-member', {'username': username}, function(data){
                data = $.parseJSON(data);
                if(data.error != undefined){
                    $('#notifications_bar').html(''+data.error+'').slideDown(200).delay(1000).slideUp(200);
                }else{
                    $('#notifications_bar').html(""+data.message+"").slideDown(200).delay(1000).slideUp(200);
                    $li.remove();
                }
            });
            return false;
        }
    });

    $('#remove-members-btn').click(function(){
        delete_token = !delete_token;
        if(delete_token){
            $('#notifications_bar').html("You can now delete members!").slideDown(200).delay(1000).slideUp(200);
            $.each($('#member-li', '#member_list'), function(index, value){
               $(value).css({
                   'border': 'solid',
                   'borderWidth': '2px',
                   'borderColor': "#e55853"
               });
            });
        }else{
            $.each($('#member-li'), function(index, value){
               $(value).css({
                   'border': 'none'
               });
            });
        }
    });

    $('#avatar-form').live('submit', function(){
        //TODO: ajax file upload
    });

    $('#create-news').click(function(){
        $('#modal-news').modal({
            opacity:80,
            overlayCss: {backgroundColor:"#5b5b5b"},
            minHeight:400,
            minWidth: 600
        });
    });

    $('#news-form').submit(function(){
        validate($(this), function(data){
            var news = data.news
            $.each(data.users, function(index, user){
                socket.emit('news-stream', {'recipient': user, 'news':news})
            })
        });

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
    });
    $('#unlike.ok').live("click", function(){
        vote("unlike", $(this), $(this).prev())
    });

    //check if u can vote
    $.each($('.alliance_content_news'), function(index, element){
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
        var username = $(this).data('username')
        console.log(username)
        var $member = $(this).prev()
        var $del = $(this)
        if(false){
        $.post('/clan/del-member', {'username': username}, function(data){
           if(data == 'ok'){
               console.log('The member has been removed!')
               $member.remove()
               $del.remove()
           }else if(data == 'failed-member'){
               console.log("This member doesn't exists")
           }else if(data == 'failed-rights'){
               console.log("You don't have rights to delete a member")
           }else{
                console.log(data)
           }
        });}

    });
});