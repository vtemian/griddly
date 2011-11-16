$(document).ready(function(){
    $('#login-form').submit(function() {
        validate($(this), function(data){
            $('#general').toast('show');
        });
        return false;
    });
    $('#register-form').submit(function() {
        validate($(this), function(data){
            if(data.not != undefined){

            }
        });
        return false;
    });
});