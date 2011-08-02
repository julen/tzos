$(document).ready(function () {

    /*
     * Tipsy tooltips
     */

    $('[rel=tipsy-ns]').tipsy({
        gravity: $.fn.tipsy.autoNS,
        live: true,
        html: true
    });
    $('[rel=tipsy-we]').tipsy({
        gravity: $.fn.tipsy.autoWE,
        live: true,
        html: true
    });

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


    /*
     * Inline tabs
     */

    $('ul.inlineTabs').tabs();


    /*
     * Show/hide stuff
     */

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

    /* Helper constants and functions */

    $DELIM = ";;;";

    $split = function (val) {
        return val.split( /,\s*/ );
    };

    $extractLast = function (term) {
        return $split(term).pop();
    }

    $('input[id$="syntrans_term"]').autocomplete({
        source: function (req, res) {
            $.getJSON($TERM_AUTOCOMPLETE_URL, {
                term: req.term,
                lang: $('select[id$="syntrans_lang"]').val(),
                sf: $('select[id$="subject_field"]').val().join(";")
            }, res);
        }
    });


    /*
     * bsmSelect for multiple select fields
     */
    $('select[id$="subject_field"], \
       select[id$="concept_origin"], \
       select[id$="product_subset"]').bsmSelect({
        removeLabel: '<strong>×</strong>',
        selectClass: 'input bsmSelect',
        containerClass: 'bsmContainer',
        listItemClass: 'b small bsmListItem',
    });

    /*
     * Tags list for multiple text inputs
     */
    $('input[id$="originating_person"]').tagit({
        tagSource: function (req, res) {
            $.getJSON($OP_AUTOCOMPLETE_URL, {
                term: $extractLast(req.term),
            }, res);
        },
        allowSpaces: true,
        singleFieldDelimiter: $DELIM
    });

    $('input[id$="entry_source"]').tagit({
        tagSource: $ES_AUTOCOMPLETE_URL,
        allowSpaces: true,
        singleFieldDelimiter: $DELIM
    });

    $('input[id$="concept_generic"], input[id$="_concept"]').tagit({
        tagSource: function (req, res) {
            $.getJSON($TERM_AUTOCOMPLETE_URL, {
                term: $extractLast(req.term),
                lang: $('select[id$="-language"]').val()||$('#langCode').val(),
                sf: $('select[id$="subject_field"]').val().join(";")
            }, res);
        },
        allowSpaces: true,
        singleFieldDelimiter: $DELIM
    });

    $('input[id$="cross_reference"]').tagit({
        tagSource: function (req, res) {
            $.getJSON($TERM_AUTOCOMPLETE_URL, {
                term: req.term,
                lang: $('select[id$="-language"]').val()||$('#langCode').val(),
                sf: $('select[id$="subject_field"]').val().join(";")
            }, res);
        },
        allowSpaces: true,
        singleFieldDelimiter: $DELIM
    });


    /*
     * FieldList population
     */
    $("p.addMore").click(function () {
        var last = $(this).parent().find("textarea").last();

        var id = last.attr("id");
        var parts = id.split("-");
        var idName = parts.slice(0, parts.length - 1).join("-");
        var idNumber = new Number(parts[parts.length-1]) + 1;
        var idNew = idName + "-" + idNumber;

        var newElem = last.clone();
        newElem.val('');
        newElem.attr('id', idNew);
        newElem.attr('name', idNew);
        newElem.insertBefore(this);
    });


    /*
     * Adding equivalents on-the-fly
     */

    // Show eqField elements that have values when reloading the page
    $("li.eqField input[value!='']").parent().show();

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
