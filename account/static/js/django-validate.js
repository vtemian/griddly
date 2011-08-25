function validate($form){
    var action = $form.attr('action')
    $.post(action, $form.serializeArray(), function(date){
        date = jQuery.parseJSON(date)
        if(date.message != undefined){
            console.log(date.message)
        }else
        if(date.ok != undefined){
                document.location = date.ok
        }else{
            $('#general', $form).empty()
            $.each(date, function(index, value){
                $('#general', $form).append('<label class="error">'+ value +'</label><br>')
            });
        }
    });
}