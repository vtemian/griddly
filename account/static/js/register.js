$(document).ready(function(){
   
    $('#register-form').submit(function() {
        validate($(this));
        return false;
    });
});