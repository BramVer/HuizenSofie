$(document).ready(function(){
	$('#filter').hide();
});


$(document).ready(function(){
	$('#options-btn').click(function(e){
		e.preventDefault();
		$("#filter").toggle(0);
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