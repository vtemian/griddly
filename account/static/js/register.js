$(document).ready(function(){
<<<<<<< HEAD
    $('#sign_up_form').ketchup({
        validateEvents: 'keyup'
    });
    $('#sign_up_form').submit(function() {
=======
   
    $('#register-form').submit(function() {
>>>>>>> fd82c93304b74f964c8e485003375f5463f47ce0
        validate($(this));
        return false;
    });
});