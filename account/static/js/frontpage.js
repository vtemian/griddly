$(document).ready(function(){
    $('#mustFixIt').live('click' , function(){
        $('#notifications_bar').html("We will fix that soon!").slideDown(200).delay(1000).slideUp(200);
    });
})