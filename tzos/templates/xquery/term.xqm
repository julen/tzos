module namespace term = "http://tzos.net/term";

import module namespace util = "http://tzos.net/util" at "util.xqm";


declare function term:owner($term as element(term))
as xs:string {
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


declare function term:norm_auth($term as element(term)) {
    $term/../termNote[@type="normativeAuthorization"]/string()
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
        <li class="meta weak">[[ _t("{ term:norm_auth($term) }") ]]</li>
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
        <li class="more">[[ _('Appears in:') ]] { term:product_subset($term) }</li>
        else () }
    </ul>
    <ul class="termActions in hideme small weak">
        {{% if g.user %}}
        <li><a href="[[ url_for('terms.add', lang='{ $termLang }', term='{ $term/string() }') ]]">[[ _('Add synonym/translation') ]]</a></li>
        {{% if g.user.owns_term('{ $termID }') %}}
        <li><a href="[[ url_for('terms.edit', id='{ $termID }') ]]">[[ _('Edit term') ]]</a></li>
        {{% endif %}}
        {{% endif %}}
    </ul>
</div>
};
