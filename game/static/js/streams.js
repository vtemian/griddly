$(document).ready(function(){
    $('#add-streams').click(function(){
        $('#choices').css('display', 'block')
    });

    $('#clan-stream-choice').click(function(){
        $('#choices').css('display', 'none')
        $.post('/profile/stream/clan', {'action': 'activate'}, function(data){
            if(data == 'ok'){
                $('#notifications_bar').html("The stream has been activated!").slideDown(200).delay(1000).slideUp(200);
                $('#stream').load('/stream/clan', function(){
                    //TODO: make stream works
                })
            }else{
                $('#notifications_bar').html(data).slideDown(200).delay(1000).slideUp(200);
            }
        })
    });

    socket.on('news-stream', function (data) {
        $('#news', '#stream').prepend(data.news)
    });

});