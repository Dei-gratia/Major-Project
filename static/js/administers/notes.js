$(document).ready(function() {
    var table = $('#notes').DataTable({
		responsive: true,
		select: false,
		columnDefs: [
            { responsivePriority: 1, targets: 0 },
            { responsivePriority: 2, targets: -2 },
			{ responsivePriority: 3, targets: -1 },
        ]
	});
	
	
	$('.dtr-control').click(function() {
		id = $(this).attr('id');
		s= $('i', this)[0]
		console.log('clicked')
		$($('i', this)[0]).toggleClass('fa-circle-plus fa-circle-minus')
		
	})

	$('#data').click(function() {
		
		$('#select-all').prop('checked', false) 
		console.log($('.selected').length)
		if($('.selected').length == 1 ) {
			$('#view').show()
			$('#edit').show()
			$('#delete').show()
			$('#verify').show()
		}
		else if( $('.selected').length > 1 ){
			$('#view').hide()
			$('#edit').hide()
			$('#delete').show()
			$('#verify').show()
		}
		else {
			$('#view').hide()
			$('#edit').hide()
			$('#delete').hide()
			$('#verify').hide()
		}
	})

	$('#select-all').on('click', function(){
		console.log('clicked')
		if ($(this).is( ":checked" )) {
			table.rows(  ).select();
			$('#delete').show()
			$('#verify').show()        
		} else {
			table.rows(  ).deselect();
			$('#view').hide()
			$('#edit').hide()
			$('#delete').hide()
			$('#verify').hide() 
		}
	 });
} );


