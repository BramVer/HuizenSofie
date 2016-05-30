$(document).ready(function(){
	$('#specs').hide();
});


$(document).ready(function(){
	$('#btnOptions').click(function(e){
		e.preventDefault();
		$("#specs").toggle(750);
	});
});

$('#btnSoort').click(function(e){
	e.preventDefault();
});

$('#btnLoc').click(function(e){
	e.preventDefault();
});

$('#btnKamer').click(function(e){
	e.preventDefault();
});

$('#btnExtra').click(function(e){
	e.preventDefault();
});

$('#btnPrijs').click(function(e){
	e.preventDefault();
});