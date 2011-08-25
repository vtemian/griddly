$(document).ready(function(){
    $('#change-password').submit(function() {
        validate($(this));
        return false;
    });
    $('input[type=text]', '#change-email').keyup(function(e){
        if(e.keyCode == 13){
            validate($('#change-email'));
        }
    })
})