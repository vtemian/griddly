$(document).ready(function(){
    
    $('#login-form').ketchup({
            validateEvents: 'keyup'
    });

    $('#login-form').submit(function() {
        validate($(this));
        return false;
    });
});