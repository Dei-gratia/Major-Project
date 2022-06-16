var sidebar = document.getElementById('sidebar')
console.log(sidebar.classList)
function sidebarUpdate() {
	var viewportWidth = window.innerWidth;
	if (viewportWidth >= 768) {
		sidebar.classList.add("show");
	} else {
		sidebar.classList.remove("show");
	}
}

window.onload = sidebarUpdate
window.onresize = sidebarUpdate

$('#top-search').focus(function() {
	$('#btn_search').removeClass('hide')
})

$('#top-search').focusout(function() {
	$('#btn_search').addClass('hide')
	
})

$(document).ready(function () {
    var table = $('#example').DataTable();
 
    $('#example tbody').on('click', 'tr', function () {
        $(this).toggleClass('table-active');
		console.log('toggled', this.name)
    });
 
    $('#button').click(function () {
        alert(table.rows('.table-active').data().length + ' row(s) selected');
    });
});

