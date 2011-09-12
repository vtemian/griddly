$(document).ready(function(){
    $('#add-streams').click(function(){
        $('#choices').css('display', 'block')
    })

    $('#clan-stream-choice').click(function(){
        $('#choices').css('display', 'none')
        $.post('/profile/stream/clan', {'action': 'activate'}, function(data){
            if(data == 'ok'){
                console.log('The stream has been activated!')
                $('#stream').load('/stream/clan', function(){
                    console.log('a')
                })
            }else{
                console.log(data)
            }
        })
    })

    socket.on('news-stream', function (data) {
        $('#news', '#stream').prepend(data.news)
    });

})