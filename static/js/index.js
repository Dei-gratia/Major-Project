$(document).ready(function() {
    var table = $('#example').DataTable( {
		responsive: true,
        buttons: [ 'copy', 'excel', 'pdf', 'colvis' ],
		select: {
            style: 'multi'
        }
    } );

	new $.fn.dataTable.FixedHeader( table );
 
    table.buttons().container()
        .appendTo( '#example_wrapper .col-md-6:eq(0)' );
} );

//$('#myModal').modal('show');
