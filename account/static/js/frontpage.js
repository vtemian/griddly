$(document).ready(function(){
    $('#mustFixIt').live('click' , function(){
        $('#notifications_bar').html("We will fix that soon!").slideDown(200).delay(1000).slideUp(200);
    });
    $('#reset-a').click(function(){
        $('#reset-password').modal({
            minHeight:100,
	        minWidth: 400
        });
    });
    $('#reset-form').submit(function(){
        var $form = $(this);
        $.modal.close();
        $('#notifications_bar').html("Reseting password...").slideDown(200).delay(1000).slideUp(200);
        $.post($form.attr('action'), $form.serializeArray(), function(data){
            data = $.parseJSON(data)
            $('#notifications_bar').html(data.message).slideDown(200).delay(1000).slideUp(200);
        });
        return false;
    });
})