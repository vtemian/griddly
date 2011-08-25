$(document).ready(function(){
    $('#login-form').submit(function() {
        validate($(this));
        return false;
    });
});