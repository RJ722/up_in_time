$(function(){
	$('.nav_button a').click(function(){
        $('.nav_button .active').removeClass('active'); // remove the class from the currently selected
        $(this).addClass('active'); // add the class to the newly clicked link
    	$(this).addClass('nav_button');
    });
});