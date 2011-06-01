module namespace term = "http://tzos.net/term";

import module namespace util = "http://tzos.net/util" at "util.xqm";


declare function term:owner($term as element(term))
{
    $term/../transacGrp[./transac[@type="transactionType"]/string()="origination" or ./transac[@type="transactionType"]/string()="input" or ./transac[@type="transactionType"]/string()="importation"]/transacNote[@type="responsibility"]/string()
};

declare function term:is_public($term as element(term))
as xs:boolean {
let $workingStatus := $term/../admin[@type="elementWorkingStatus"]/string()
return $workingStatus != "starterElement" and $workingStatus != "importedElement" and $workingStatus != "archiveElement"
};


declare function term:asLink($term as element(term))
as element(a) {
    <a href="[[ url_for('terms.detail', id='{ data($term/@id) }') ]]">{ $term/string() }</a>
};

declare function term:asLink2($term_str as xs:string)
as element(a) {
    let $term := collection($collection)//term[string()=$term_str]
    return term:asLink($term)
};


declare function term:synonyms($term as element(term))
as element(a)* {
    for $syn in $term/../..//term[string()!=$term/string()]
    let $workingStatus := $syn/../admin[@type="elementWorkingStatus"]/string()
    where $workingStatus != "starterElement" and $workingStatus != "importedElement"
    return term:asLink($syn)
};


declare function term:translations($term as element(term))
{
    for $trans in $term/../../..//term
    let $termLang := data($term/../../@xml:lang)
    let $transLang := data($trans/../../@xml:lang)
    let $workingStatus := $trans/../admin[@type="elementWorkingStatus"]/string()
    where $trans/../..[@xml:lang!=$termLang] and $workingStatus != "starterElement" and $workingStatus != "importedElement"
    return (
    <dt>{ $transLang }</dt>,
    <dd lang="{ $transLang }">{ term:asLink($trans) }</dd>)
};


declare function term:type($term as element(term)) {
    $term/../termNote[@type="termType"]/string()
};


declare function term:pos($term as element(term)) {
    $term/../termNote[@type="partOfSpeech"]/string()
};


declare function term:admn_sts($term as element(term)) {
    $term/../termNote[@type="administrativeStatus"]/string()
};


declare function term:norm_auth($term as element(term)) {
    (: TODO: Remove [1] once we make sure there will be a single element :)
    $term/../termNote[@type="normativeAuthorization"][1]/string()
};


declare function term:norm_auth_org($term as element(term)) {
    let $nao := $term/../termNote[@type="normativeAuthorization"]/data(@target)
    return collection($collection)//refObjectList[@type="respOrg"]/refObject[@id=$nao]/item[@type="org"]/string()
};


declare function term:concept_origin($term as element(term)) {
    $term/../admin[@type="conceptOrigin"]/string()
};


declare function term:orig_person($term as element(term)) {
    $term/../admin[@type="originatingPerson"]/string()
};


declare function term:product_subset($term as element(term)) {
    $term/../admin[@type="productSubset"]/string()
};


declare function term:working_status($term as element(term)) {
    $term/../admin[@type="elementWorkingStatus"]/string()
};


declare function term:entry_source($term as element(term)) {
    $term/../admin[@type="entrySource"]/string()
};


declare function term:subject_field($term as element(term)) {
    $term/../../../descrip[@type="subjectField"]/string()
};


declare function term:subordinate_cg($term as element(term)) {
    $term/../../../descrip[@type="subordinateConceptGeneric"]/string()
};


declare function term:superordinate_cg($term as element(term)) {
    $term/../../../descrip[@type="superordinateConceptGeneric"]/string()
};


declare function term:antonym_concept($term as element(term)) {
    $term/../../../descrip[@type="antonymConcept"]/string()
};


declare function term:related_concept($term as element(term)) {
    $term/../../../descrip[@type="relatedConcept"]/string()
};


declare function term:definition($term as element(term)) {
    $term/../../descrip[@type="definition"]/string()
};


declare function term:context($term as element(term)) {
    $term/../descrip[@type="context"]/string()
};


declare function term:example($term as element(term)) {
    $term/../descrip[@type="example"]/string()
};


declare function term:explanation($term as element(term)) {
    $term/../descrip[@type="explanation"]/string()
};


declare function term:xref($term as element(term)) {
    $term/../ref[@type="crossReference"]/string()
};

declare function term:xref_id($term as element(term)) {
    $term/../ref[@type="crossReference"]/data(@target)
};


declare function term:display($term as element(term)) {
let $termLang := data($term/../../@xml:lang)
let $termID := data($term/@id)
return
<div class="term">
    <ul class="term">
        <li class="term">{ term:asLink($term) }</li>
        { if (term:type($term)) then
        <li class="meta weak">[[ _t("{ term:type($term) }") ]]</li>
        else () }
        { if (term:pos($term)) then
        <li class="meta weak">[[ _t("{ term:pos($term) }") ]]</li>
        else () }
        { if (term:norm_auth($term)) then
        <li class="meta weak">[[ _t("{ term:norm_auth($term) }") ]] ({ term:norm_auth_org($term) })</li>
        else () }
        <li>
        { (: If any, display synonyms :)
            let $syns := term:synonyms($term)
            return
            if (exists($syns)) then
                <dl class="syn">
                    <dt class="in"><abbr class="small" title="[[ _('Synonyms') ]]">[[ _('syn.') ]]</abbr></dt>
                    <dd class="in">{ util:join_seq($syns) }</dd>
                </dl>
            else ()
        }
            <dl class="trans">{ term:translations($term) }</dl>
        </li>
        <li class="more">[[ _('Origin:') ]] { term:concept_origin($term) }
            { if (term:orig_person($term)) then
                <span class="weak"> ({ term:orig_person($term) })</span>
              else () }</li>
        { if (term:product_subset($term)) then
        <li class="more">[[ _('Appears in:') ]] [[ _t("{ term:product_subset($term) }") ]]</li>
        else () }
        { if (term:subject_field($term)) then
        <li class="more">[[ _('Classification:') ]]
        {
            let $fields :=
                for $field in tokenize(term:subject_field($term), ";")
                return <span>[[ _t("{ $field }") ]]</span>
            return util:join_seq($fields)
        }
        </li>
        else () }
        { if (term:subordinate_cg($term)) then
        <li class="more">[[ _('Hyponym:') ]] { term:asLink2(term:subordinate_cg($term)) }</li>
        else () }
        { if (term:superordinate_cg($term)) then
        <li class="more">[[ _('Hypernym:') ]] { term:asLink2(term:superordinate_cg($term)) }</li>
        else () }
        { if (term:antonym_concept($term)) then
        <li class="more">[[ _('Antonym:') ]] { term:asLink2(term:antonym_concept($term)) }</li>
        else () }
        { if (term:related_concept($term)) then
        <li class="more">[[ _('Related concept:') ]] { term:asLink2(term:related_concept($term)) }</li>
        else () }
        { if (term:xref($term)) then
        <li class="more">[[ _('See also:') ]] <a href="[[ url_for('terms.detail', id='{ term:xref_id($term) }') ]]">{ term:asLink2(term:xref($term)) }</a></li>
        else () }
    </ul>
    <ul class="termActions in small">
        {{% if g.user %}}
        <li><a href="[[ url_for('terms.add', lang='{ $termLang }', term='{ $term/string() }') ]]">[[ _('Add synonym/translation') ]]</a></li>
        {{% if g.user.owns_term('{ $termID }') %}}
        <li><a href="[[ url_for('terms.edit', id='{ $termID }') ]]">[[ _('Edit term') ]]</a></li>
        {{% endif %}}
        {{% endif %}}
    </ul>
</div>
};


declare function term:values($term as element(term)) {
string-join(
    ($term/data(@id), (: term ID :)
     $term/../../data(@xml:lang), (: language of the term :)
     $term/string(), (: actual term :)
     term:concept_origin($term),
     term:subject_field($term),
     term:orig_person($term),
     term:definition($term),
     term:context($term),
     term:example($term),
     term:explanation($term),
     term:entry_source($term),
     term:xref($term),
     term:product_subset($term),
     term:norm_auth($term),
     term:norm_auth_org($term),
     term:subordinate_cg($term),
     term:superordinate_cg($term),
     term:antonym_concept($term),
     term:related_concept($term),
     term:pos($term),
     term:type($term),
     term:admn_sts($term)
     ), ";")
};
