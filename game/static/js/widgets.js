$(document).ready(function(){
    /* Widget */

	/* Widget opacity */

	$('#widget').mouseenter(function(){
		$(this).animate({opacity:1},100);
		});

	$('#widget').mouseleave(function(){
		$(this).animate({opacity:0.9},100);
		});

	/* Widget start + stop position */

	$('#widget').draggable({

    // Find original position of dragged image.
    start: function(event, ui) {

        // Show start dragged position of image.
        var start_position = $(this).position();
    },

    // Find position where image is dropped.
    stop: function(event, ui) {

        // Show dropped position.
        var stop_position = $(this).position();
        console.log(stop_position.top)
        $.post('/profile/widget-lvl', {'top': stop_position.top, 'left': stop_position.left}, function(data){
            if(data == 'ok'){
                console.log('The position has been saved ;)')
            }else{
                console.log(data)
            }
        })
    }
	, containment: "#map_holder", scroll: false});



    /* ============================================================= */


    /* Widget */

    /* Widget opacity */

	$('#territory_widget').mouseenter(function(){
		$(this).animate({opacity:1},100);
		});

	$('#territory_widget').mouseleave(function(){
		$(this).animate({opacity:0.9},100);
		});

    /* Widget territory info */

    $('li','#territory_widget_tabs').first().toggleClass('active_territory');
    $('.territory_widget_territory').first().css("display", "block");
    /* Widget checkins dropdown */

    $('#show_checkins').click(function(){
        $('#territory_widget_checkins').stop(true,true).slideToggle(200);
    });

    /* Widget venues slideout */

    $('#show_venues').click(function(){
        $('.territory_widget_venues').stop(true,true).slideToggle(200);
    });



	/* Widget start + stop position */

	$('#territory_widget').draggable({

    // Find original position of dragged image.
    start: function(event, ui) {

        // Show start dragged position of image.
        var start_position = $(this).position();
    },

    // Find position where image is dropped.
    stop: function(event, ui) {

        // Show dropped position.
        var stop_position = $(this).position();
        console.log(stop_position.top)
        $.post('/profile/widget-lvl', {'top': stop_position.top, 'left': stop_position.left}, function(data){
            if(data == 'ok'){
                console.log('The position has been saved ;)')
            }else{
                console.log(data)
            }
        })
    }
	, containment: "#map_holder", scroll: false});
});