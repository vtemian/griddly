function validate($form, callback){
    var action = $form.attr('action')
    $.post(action, $form.serializeArray(), function(date){
        date = jQuery.parseJSON(date)
        if(date.message != undefined){
            $('#general', $form).empty()
            console.log(date.message)
            $('#bara_p').html(date.message)
        }else
        if(date.ok != undefined){
            document.location = date.ok
        }else{
            $('#general', $form).empty()
            $.each(date, function(index, value){
                $('#general', $form).append('<label class="error">'+ value +'</label><br>')
            });
        }
        if(typeof callback == 'function'){
            callback.call(this, date);
        }
    });
    return false;
}