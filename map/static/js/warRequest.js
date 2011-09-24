$(document).ready(function(){
    $('#warRequest').live('click', function(){
        var username = $(this).data('username')
        var id = $(this).data('id')
        console.log(id)
        $.post('/battle/request/war', {'username': username, 'id': id}, function(data){
            var obj = jQuery.parseJSON(data)
            if(obj.nice != undefined){
                console.log(obj.nice)
            }else{
                console.log(obj.error);
            }
        })
    });
})