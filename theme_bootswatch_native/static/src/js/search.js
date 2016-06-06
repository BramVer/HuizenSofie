$(document).ready(function(){
	$('#specs').hide();
});


$(document).ready(function(){
	$('#btnOptions').click(function(e){
		e.preventDefault();
		$("#specs").toggle(750);
	});
});


$(document).ready(function(){
	$('#text').hide();
	$('#ebookOverlay').hide();
	$('#ebookSec').hover(function() {
    	$(this).addClass('transition');
    	$('#text').show(300);

	}, function() {
    	$(this).removeClass('transition');
    	$('#text').hide(500);
	});
	$('#ebookSec').click(function(){
		$('#ebookOverlay').show( {direction: "right"}, 500);
	});
	$('#btnExit').click(function(){
		$('#ebookOverlay').hide(500);
	})
});
