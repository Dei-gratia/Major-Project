var sidebar = document.getElementById('sidebar')
console.log(sidebar.classList)
function sidebarUpdate() {
	var viewportWidth = window.innerWidth;
	if (viewportWidth >= 768) {
		sidebar.classList.add("show");
		sidebar.classList.remove("hide");
	} else {
		sidebar.classList.remove("show");
		sidebar.classList.add('hide')
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


