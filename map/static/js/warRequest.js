$(document).ready(function(){
    $('#warRequest').live('click', function(){
        var username = $(this).data('username')
        $.post('/battle/request/war', {'username': username}, function(data){
            var obj = jQuery.parseJSON(data)
            if(obj.nice != undefined){
                console.log(obj.nice)
            }else{
                console.log(obj.error)
            }
        })
    });
})