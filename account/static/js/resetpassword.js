$(document).ready(function(){
   $('#password-form').submit(function(){
       var $form = $(this);
       validate($form, function(){
           setTimeout(function() {
              window.location.href = "/";
            }, 400);
       });
       return false;
   });
});