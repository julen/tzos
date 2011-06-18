$(document).ready(function () {

    $('[rel=tipsy-ns]').tipsy({gravity: $.fn.tipsy.autoNS, live: true});
    $('[rel=tipsy-we]').tipsy({gravity: $.fn.tipsy.autoWE, live: true});

    /* Dropdown for picking glossary language */
    $('#tzosDict > a').click(function (e) {
        e.preventDefault();
    });
    $('#tzosDict').click(function (e) {
        e.stopPropagation();
        $(this).children('ul').toggle();
    });
    $('body').not('#tzosDict').click(function (e) {
        if ($('ul.dictList').is(':visible')) {
            $('ul.dictList').hide();
        }
    });

    $('ul.inlineTabs').tabs();

    if ($('li.showSource input:checkbox').is(':checked')) {
        $('li.showSource').next('li').removeClass('hideme');
    }
    if ($('li.showSyntrans input:checkbox').is(':checked')) {
        $('li.showSyntrans').nextAll('li').removeClass('hideme');
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
        $('li.showSource').next('li').toggle('slow');
    });
    $('li.showSyntrans input:checkbox').click(function () {
        $('li.showSyntrans').nextAll('li').toggle('slow');
    });

    $("input#entry_source").autocomplete({
        source: $AUTOCOMPLETE_URL + '?type=entrySource'
    });

    $("select#add-subject_field, \
       .editTerm select#subject_field, \
       select#upload-subject_field").bsmSelect({
        removeLabel: '<strong>X</strong>',
        selectClass: 'input bsmSelect',
        containerClass: 'bsmContainer',
        listItemClass: 'b small bsmListItem',
    });

    $("a.addCol").click(function () {
        var newEl = $("ul.otherFields > li:first-child").clone(true);
        newEl.insertAfter("ul.otherFields > li:last-child").show();
    });

    $("a.rmCol").click(function () {
        $(this).parent().remove();
    });

    $("#upload-submit").click(function () {
        var cols = $("li:visible select#upload-other_fields option:selected").
        map(function (i) {
            return $(this).val() + "-" + i;
        }).toArray().join(";");

        $("#upload-columns").val(cols)
    });

});
