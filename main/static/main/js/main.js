$(function() {

	$('#toggle_signUp').click(function(){
		$('#signIn').modal('hide');
		$('#signUp').modal('show');
	});

	$('#toggle_logIn').click(function(){
		$('#signUp').modal('hide');
		$('#signIn').modal('show');
	});

  var width = window.innerWidth;
  if(width < 767){
    $('.view-answer a').removeClass('pull-right');
  }
	
});


