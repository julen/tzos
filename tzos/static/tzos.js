$(document).ready(function () {

    $('[rel=tipsy-ns]').tipsy({gravity: $.fn.tipsy.autoNS});
    $('[rel=tipsy-we]').tipsy({gravity: $.fn.tipsy.autoWE});

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
        $('ul.extraFields').toggle('slow');
    });

    $('li.showSource input:checkbox').click(function () {
        $(this).parent().next('li').toggle('slow');
    });
});
