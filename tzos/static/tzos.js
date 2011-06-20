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

    /*
     * Autocompletes
     */
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

    /*
     * Adding equivalents on-the-fly
     */

    // Disable selected option if the eqterm-* field is visible
    $('li.eqField:visible input').each(function () {
        var val = $(this).attr('id');
        var lang = val.split("-");
        lang = lang[lang.length - 1];

        $(".eqFields select")
            .find('option[value="' + lang + '"]')
            .attr('disabled', 'disabled');
    });

    $(".addEq").change(function () {

        var value = $(this).val();

        // Ignore action if the selection is the placeholder
        if (value == "") {
            return false;
        }

        // Disable selected option and display its form field
        $('option[value="' + value + '"]', this).
            attr('disabled', 'disabled');
        $('#add-eqterm-' + value).parent().show();

        // Finally, reset current selection
        $(this).val("");
    });
    $("a.rmEq").click(function () {
        var input = $(this).parent().find("input");
        var val = $(input).attr("id");
        var lang = val.split("-");
        lang = lang[lang.length - 1];

        // Enable selecting the option again
        $(".eqFields select")
            .find('option[value="' + lang + '"]')
            .removeAttr('disabled');

        // Remove any data previously set and hide the form field
        $(input).val("");
        $(this).parent().hide();
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
