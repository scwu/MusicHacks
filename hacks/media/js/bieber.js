$(document).ready(function(){
	people = [
		"Justin Bieber",
		"Jay-Z",
		"Kanye West",
		"Psy",
	];

	cur = 0;
	count = people.length;

	interval = setInterval(function(){
		if(cur == (count - 1)) {
			cur = 0;
		} else {
			cur++; // = cur + 1;
		}
//		$('.bieber').
		$('.bieber').fadeOut(function(){
			$('.bieber').text(people[cur]);
			$('.bieber').fadeIn();
		})
	}, 3000);

	console.log('yo')
});