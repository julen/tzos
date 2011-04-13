$(document).ready(function () {
    $('#tzosDict > a').click(function (e) {
        e.preventDefault();
    });
    $('#tzosDict').hover(function () {
        $(this).children('ul').toggle();
    });
    $('ul.inlineTabs').tabs();

    $('.showme').show();
    $('.hideme').hide();

    $('.showFields').click(function () {
        if ($(this).prev().hasClass('iBRarr')) {
            $(this).prev().removeClass('iBRarr').addClass('iBDarr');
        } else {
            $(this).prev().removeClass('iBDarr').addClass('iBRarr');
        }
        $('.extraFields').toggle('slow');
    });
});
