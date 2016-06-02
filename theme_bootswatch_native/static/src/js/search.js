$(document).ready(function(){
	$('#specs').hide();
});


$(document).ready(function(){
	$('#btnOptions').click(function(e){
		e.preventDefault();
		$("#specs").toggle(750);
	});
});

