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

    if ($('li.showSource input:checkbox').is(':checked')) {
        $('li.showSource').next('li').removeClass('hideme');
    }
    if ($('li.showSyntrans input:checkbox').is(':checked')) {
        $('li.showSyntrans').nextAll('li').removeClass('hideme');
    }

    $('div.nonDefault').removeClass('hideme');

    $('.showme').show();
    $('.hideme').hide();

    $('.showHide').click(function () {
        if ($(this).prev().hasClass('iBRarr')) {
            $(this).prev().removeClass('iBRarr').addClass('iBDarr');
        } else {
            $(this).prev().removeClass('iBDarr').addClass('iBRarr');
        }
        $('div.extra').toggle('slow');
    });

    $('li.showSource input:checkbox').click(function () {
        $(this).parent().next('li').toggle('slow');
    });
    $('li.showSyntrans input:checkbox').click(function () {
        $(this).parent().nextAll('li').toggle('slow');
    });

    $("input#entry_source").autocomplete({
        source: '/xhr/autocomplete/?type=entrySource'
    });

});
