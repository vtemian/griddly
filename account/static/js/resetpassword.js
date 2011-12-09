$(document).ready(function(){
   $('#password-form').submit(function(){
       var $form = $(this);
       validate($form);
       return false;
   });
});