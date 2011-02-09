$(document).ready(function () {
    $('#tzosDict').click(function (e) {
        e.preventDefault();
    });
    $('#tzosDict').hover(function () {
        $(this).children('ul').toggle();
    });
});
