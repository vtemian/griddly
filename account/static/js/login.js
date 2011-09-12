$(document).ready(function(){
<<<<<<< HEAD
    $('#login-btn').click(function(){
       $('#login-div').modal({
           opacity:80,
			overlayCss: {backgroundColor:"#5b5b5b"},
            minHeight:400,
	        minWidth: 600,
       })
    });


    $('#login-form').ketchup({
            validateEvents: 'keyup'
    });

=======
>>>>>>> fd82c93304b74f964c8e485003375f5463f47ce0
    $('#login-form').submit(function() {
        validate($(this));
        return false;
    });
});