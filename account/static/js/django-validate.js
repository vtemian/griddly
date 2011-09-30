function validate($form, callback){
    var action = $form.attr('action')
    $.post(action, $form.serializeArray(), function(date){
        date = jQuery.parseJSON(date)
        if(date.message != undefined){
            $('#general', $form).empty()
            $('#notifications_bar').html(date.message).slideDown(200).delay(1000).slideUp(200);
        }else
        if(date.ok != undefined){
            document.location = date.ok
        }else{
            console.log('a', date)

            $('#general', $form).empty()
            $.each(date, function(index, value){
                console.log(value)
                $('#general', $form).append('<label class="error">'+ value +'</label><br>')
            });
        }
        if(typeof callback == 'function'){
            callback.call(this, date);
        }
    });
    return false;
}