var i= $('#levels').val()
console.log(i)

if(i=="College") 
{
	console.log("in if college")
	$('#specialization').hide()
	$('#program').show()
}
else if(i=="A(Advanced) Level")
{
	$('#program').hide() 
	$('#specialization').show() 

}
else {
	$('#specialization').hide()
	$('#program').hide()
}

$('#levels').bind('change', function(event) {
	console.log("in change")
	var i= $('#levels').val()
	console.log(i)
	

	if(i=="College") 
	{
		console.log("in if college")
		$('#specialization').hide()
		$('#program').show()
	}
	else if(i=="A(Advanced) Level")
	{
		$('#program').hide() 
		$('#specialization').show() 
	}
	else {
		$('#program').hide() 
		$('#specialization').hide() 
	}
	
})

$(".rating a").on('click', function(e){
	let value = $(this).data('value');
	console.log(value)
   $.ajax({
      url: "some_url",
      type: 'POST',
      data: {'rating': value},
      success: function (d){
       // some processing
      }
   })
});