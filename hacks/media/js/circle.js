var circle = {
	state: "idle",
};

$(document).ready(function (){

	// listen for record button click, fire event
	$('#record-button').on('click', function(){
		if (circle.state == "idle") {
			circle.state = "active";
			//change icon
			$(this).find('i').removeClass('icon-microphone');
			$(this).find('i').addClass('icon-stop');
			$(this).find('span').text('stop');
			record();
		} else {
			stop();
			upload();
			$(this).find('i').removeClass('icon-stop');
			$(this).find('i').addClass('icon-microphone');
			$(this).find('span').text('record');
		}
	});

	$('#upload-button').on('click', function(){
		upload();
	});
});
