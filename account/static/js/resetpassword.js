$(document).ready(function(){
   $('#password-form').submit(function(){
       var $form = $(this);
       validate($form, function(data){
           console.log(data);
       });
       return false;
   });
});