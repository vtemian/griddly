$(document).ready(function(){
    $('#register-form').ketchup({
        validateEvents: 'keyup'
    });
    $('#register-form').submit(function() {
        validate($(this));
        return false;
    });
});