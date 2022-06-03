simpleslider.getSlider({
	container: document.getElementById('popular_slider'),
	prop: 'top',
	init: -25,
	duration: 1,
	delay: 5,
	show: 0,
	end: 25,
	unit: 'px'
  });

  function myFunction() {
	var x = document.getElementById("password");
	if (x.type === "password") {
	  x.type = "text";
	} else {
	  x.type = "password";
	}
  }