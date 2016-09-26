$(function(){
	$('.nav_button a').click(function(){
        $('.nav_button .active').removeClass('active'); // remove the class from the currently selected
        $(this).addClass('active'); // add the class to the newly clicked link
    	$(this).addClass('nav_button');
    });
});


$(window).scroll(function() {
  if ($(document).scrollTop() > 25) {
    $('.header_main').addClass('shrink');
    $('.nav_button ').addClass('shrink');
    $('#nav_bar_right tr').addClass('shrink')
  } else {
    $('.header_main').removeClass('shrink');
    $('.nav_button ').removeClass('shrink');
    $('#nav_bar_right tr').removeClass('shrink')
  }
});