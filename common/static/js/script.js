/* Author: */


(function(){
	
	var angle = 0;
setInterval(function(){
      angle+=3;
     $("#user_notifications").rotate(angle);
},10);
		
	/*Login Modal*/
	$("#login_button").click(function(){
		$('#login_modal')
		.modal({
			opacity:80,
			overlayCss: {backgroundColor:"#5b5b5b"}	
		});
	});
	
	/*Register Modal*/
	$("#register_button").click(function(){
		$('#register_modal')
		.modal({
			opacity:80,
			overlayCss: {backgroundColor:"#5b5b5b"}	
		});
	});
	
	/*Register Description Toggle*/
	 $("#register_description_toggle").click(function () {
      $("#register_description")
		  .slideToggle()
		  .css({'display':'block'})
		  .stop(true,true);  
    });
		
	/*Menu Tooltips*/
	$('a','#menu_list').tipsy({gravity: 's' , fade:'true'});
	/*Badges Tooltips*/
	$('a','#badges_list').tipsy({gravity: 'n' });
	
	/* User Menu Subnav */
	
	 $("#user_menu").mouseover(function() {
   	 $("#subnav_wrap").css('display','block');
  }).mouseout(function(){
    $("#subnav_wrap").css('display','none');
  });
  
  /* Map Settings Toggle */
  
  $("#map_settings_button_toggle").click(function () {
      $("#map_settings_buttons_wrapper").slideToggle().stop(true,true);
    });
	
  /* Map Filters Toggle */	
  
  $("#map_filters_button_toggle").click(function () {
      $("#map_filters_buttons_wrapper").slideToggle().stop(true,true);
    });
	
	
	 
})(jQuery);

























