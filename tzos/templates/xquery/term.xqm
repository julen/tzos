module namespace term = "http://tzos.net/term";

import module namespace util = "http://tzos.net/util" at "util.xqm";


declare function term:owner($tig as element(tig))
{
    $tig/transacGrp[./transac[@type="transactionType"]/string()="origination" or ./transac[@type="transactionType"]/string()="input" or ./transac[@type="transactionType"]/string()="importation"]/transacNote[@type="responsibility"]/string()
};

declare function term:is_public($tig as element(tig))
as xs:boolean {
let $workingStatus := term:working_status($tig)
return $workingStatus != "starterElement" and $workingStatus != "importedElement" and $workingStatus != "archiveElement"
};

declare function term:term($tig as element(tig)) {
    $tig/term/string()
};


declare function term:asLink($tig as element(tig))
as element(a) {
    <a href="[[ url_for('terms.detail', id='{ data($tig/@id) }') ]]">{ term:term($tig) }</a>
};

declare function term:asLink2($term_str as xs:string)
as element(a) {
    let $tig := collection($collection)//tig[term/string()=$term_str]
    return term:asLink($tig)
};


declare function term:synonyms($tig as element(tig))
as element(a)* {
    for $syn in $tig/..//tig[term/string()!=term:term($tig)]
    let $workingStatus := term:working_status($syn)
    where $workingStatus != "starterElement" and $workingStatus != "importedElement"
    return term:asLink($syn)
};


declare function term:translations($tig as element(tig))
{
    for $trans in $tig/../..//tig
    let $termLang := data($tig/../@xml:lang)
    let $transLang := data($trans/../@xml:lang)
    let $workingStatus := term:working_status($trans)
    where $trans/..[@xml:lang!=$termLang] and $workingStatus != "starterElement" and $workingStatus != "importedElement"
    return (
    <dt>{ $transLang }</dt>,
    <dd lang="{ $transLang }">{ term:asLink($trans) }</dd>)
};


declare function term:type($tig as element(tig)) {
    $tig/termNote[@type="termType"]/string()
};


declare function term:pos($tig as element(tig)) {
    $tig/termNote[@type="partOfSpeech"]/string()
};


declare function term:admn_sts($tig as element(tig)) {
    $tig/termNote[@type="administrativeStatus"]/string()
};


declare function term:norm_auth($tig as element(tig)) {
    $tig/termNote[@type="normativeAuthorization"]/string()
};


declare function term:norm_auth_org($tig as element(tig)) {
    let $nao := $tig/termNote[@type="normativeAuthorization"]/data(@target)
    return collection($collection)//refObjectList[@type="respOrg"]/refObject[@id=$nao]/item[@type="org"]/string()
};


declare function term:concept_origin($tig as element(tig)) {
    $tig/admin[@type="conceptOrigin"]/string()
};


declare function term:orig_person($tig as element(tig)) {
    $tig/admin[@type="originatingPerson"]/string()
};


declare function term:product_subset($tig as element(tig)) {
    $tig/admin[@type="productSubset"]/string()
};


declare function term:working_status($tig as element(tig)) {
    $tig/admin[@type="elementWorkingStatus"]/string()
};


declare function term:entry_source($tig as element(tig)) {
    $tig/admin[@type="entrySource"]/string()
};


declare function term:subject_field($tig as element(tig)) {
    $tig/../../descrip[@type="subjectField"]/string()
};


declare function term:subordinate_cg($tig as element(tig)) {
    $tig/../../descrip[@type="subordinateConceptGeneric"]/string()
};


declare function term:superordinate_cg($tig as element(tig)) {
    $tig/../../descrip[@type="superordinateConceptGeneric"]/string()
};


declare function term:antonym_concept($tig as element(tig)) {
    $tig/../../descrip[@type="antonymConcept"]/string()
};


declare function term:related_concept($tig as element(tig)) {
    $tig/../../descrip[@type="relatedConcept"]/string()
};


declare function term:definition($tig as element(tig)) {
    $tig/../descrip[@type="definition"]/string()
};


declare function term:context($tig as element(tig)) {
    $tig/descrip[@type="context"]/string()
};


declare function term:example($tig as element(tig)) {
    $tig/descrip[@type="example"]/string()
};


declare function term:explanation($tig as element(tig)) {
    $tig/descrip[@type="explanation"]/string()
};


declare function term:xref($tig as element(tig)) {
    $tig/ref[@type="crossReference"]/string()
};

declare function term:xref_id($tig as element(tig)) {
    $tig/ref[@type="crossReference"]/data(@target)
};


declare function term:display($tig as element(tig)) {
let $termLang := data($tig/../@xml:lang)
let $termID := data($tig/@id)
return
<div class="term">
    <ul class="term">
        <li class="term">{ term:asLink($tig) }</li>
        { if (term:type($tig)) then
        <li class="meta weak">[[ _t("{ term:type($tig) }") ]]</li>
        else () }
        { if (term:pos($tig)) then
        <li class="meta weak">[[ _t("{ term:pos($tig) }") ]]</li>
        else () }
        { if (term:norm_auth($tig)) then
        <li class="meta weak">[[ _t("{ term:norm_auth($tig) }") ]] ({ term:norm_auth_org($tig) })</li>
        else () }
        <li>
        { (: If any, display synonyms :)
            let $syns := term:synonyms($tig)
            return
            if (exists($syns)) then
                <dl class="syn">
                    <dt class="in"><abbr class="small" title="[[ _('Synonyms') ]]">[[ _('syn.') ]]</abbr></dt>
                    <dd class="in">{ util:join_seq($syns) }</dd>
                </dl>
            else ()
        }
            <dl class="trans">{ term:translations($tig) }</dl>
        </li>
        <li class="more">[[ _('Origin:') ]] { term:concept_origin($tig) }
            { if (term:orig_person($tig)) then
                <span class="weak"> ({ term:orig_person($tig) })</span>
              else () }</li>
        { if (term:product_subset($tig)) then
        <li class="more">[[ _('Appears in:') ]] [[ _t("{ term:product_subset($tig) }") ]]</li>
        else () }
        { if (term:subject_field($tig)) then
        <li class="more">[[ _('Classification:') ]]
        {
            let $fields :=
                for $field in tokenize(term:subject_field($tig), ";")
                return <span>[[ _t("{ $field }") ]]</span>
            return util:join_seq($fields)
        }
        </li>
        else () }
        { if (term:subordinate_cg($tig)) then
        <li class="more">[[ _('Hyponym:') ]] { term:asLink2(term:subordinate_cg($tig)) }</li>
        else () }
        { if (term:superordinate_cg($tig)) then
        <li class="more">[[ _('Hypernym:') ]] { term:asLink2(term:superordinate_cg($tig)) }</li>
        else () }
        { if (term:antonym_concept($tig)) then
        <li class="more">[[ _('Antonym:') ]] { term:asLink2(term:antonym_concept($tig)) }</li>
        else () }
        { if (term:related_concept($tig)) then
        <li class="more">[[ _('Related concept:') ]] { term:asLink2(term:related_concept($tig)) }</li>
        else () }
        { if (term:xref($tig)) then
        <li class="more">[[ _('See also:') ]] <a href="[[ url_for('terms.detail', id='{ term:xref_id($tig) }') ]]">{ term:asLink2(term:xref($tig)) }</a></li>
        else () }
    </ul>
    <ul class="termActions in small">
        {{% if g.user %}}
        <li><a href="[[ url_for('terms.add', lang='{ $termLang }', term='{ term:term($tig) }') ]]">[[ _('Add synonym/translation') ]]</a></li>
        {{% if g.user.owns_term('{ $termID }') %}}
        <li><a href="[[ url_for('terms.edit', id='{ $termID }') ]]">[[ _('Edit term') ]]</a></li>
        {{% endif %}}
        {{% endif %}}
    </ul>
</div>
};


declare function term:values($tig as element(tig)) {
string-join(
    ($tig/data(@id), (: term ID :)
     $tig/../data(@xml:lang), (: language of the term :)
     term:term($tig),
     term:concept_origin($tig),
     term:subject_field($tig),
     term:orig_person($tig),
     term:definition($tig),
     term:context($tig),
     term:example($tig),
     term:explanation($tig),
     term:entry_source($tig),
     term:xref($tig),
     term:product_subset($tig),
     term:norm_auth($tig),
     term:norm_auth_org($tig),
     term:subordinate_cg($tig),
     term:superordinate_cg($tig),
     term:antonym_concept($tig),
     term:related_concept($tig),
     term:pos($tig),
     term:type($tig),
     term:admn_sts($tig)
     ), ";")
};
