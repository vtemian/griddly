$(document).ready(function(){

    $('#login-form').submit(function(){
        var form = $(this);
        var action = $(this).attr('post-data')
        $.post(action, $(this).serializeArray(), function(data){
            if(data == 'ok'){
                document.location = '/game'
            }else if(data == 'disabled'){
                $('.error' ,form).html("This account has been disable!");
            }else if(data == 'not'){
                $('.error' ,form).html("Incorect username or password!");
            }
            return false;
        });
        return false;
    });

    $('#register-form').ketchup({
        validateEvents: 'keyup'
    });
});