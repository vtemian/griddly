var limit = 10;
var increment = 10;
var rank = 1;
function get_ranks(limit){
    $.get('/get-ranks/'+limit, function(data){
        $('#ranks_list').append(data);
        if(data != ''){
            $.each($('#rank-place', '#ranks_list').get(), function(index, value){
                $(value).html(rank);
                $(value).attr('id', 'rank-placed');
                rank++;
            });
        }
    });
}
$(window).scroll(function(){
    if  ($(window).scrollTop() == $(document).height() - $(window).height()){
       get_ranks(limit);
        limit += increment;
    }
});

$(document).ready(function(){
    get_ranks(limit);
    limit += increment;
});