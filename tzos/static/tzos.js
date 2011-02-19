$(document).ready(function () {
    $('#tzosDict > a').click(function (e) {
        e.preventDefault();
    });
    $('#tzosDict').hover(function () {
        $(this).children('ul').toggle();
    });
    $('ul.inlineTabs').tabs();
});
