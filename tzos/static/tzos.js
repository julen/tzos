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
        $(this).next('li').removeClass('hideme');
    }
    if ($('li.showSyntrans input:checkbox').is(':checked')) {
        $(this).parent().nextAll('li').removeClass('hideme');
    }

    $('div.doNotHide').removeClass('hideme');

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
        source: $AUTOCOMPLETE_URL + '?type=entrySource'
    });

    $("select#add-subject_field, \
       select#edit-subject_field, \
       select#upload-subject_field").bsmSelect({
        removeLabel: '<strong>X</strong>',
        selectClass: 'input bsmSelect',
        containerClass: 'bsmContainer',
        listItemClass: 'b small bsmListItem',
    });

});
