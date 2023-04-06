$(document).ready(function () {
    let sidebar = $('#sidebar');
    let sidebarCollapse = $('#sidebarCollapse');


    if (window.innerWidth < 768) {
        sidebar.removeClass('active')
    }

    sidebarCollapse.on('click', function () {
        sidebar.toggleClass('active');
    });

});
