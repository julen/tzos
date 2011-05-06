module namespace term = "http://tzos.net/term";


declare function term:owner($term as element(term))
as xs:string {
    $term/../transacGrp[./transac[@type="transactionType"]/string()="origination" or ./transac[@type="transactionType"]/string()="input" or ./transac[@type="transactionType"]/string()="importation"]/transacNote[@type="responsibility"]/string()
};

declare function term:is_public($term as element(term))
as xs:boolean {
let $workingStatus := $term/../admin[@type="elementWorkingStatus"]/string()
return $workingStatus != "starterElement" and $workingStatus != "importedElement"
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


declare function term:display($term as element(term)) {
let $termLang := data($term/../../@xml:lang)
let $termID := data($term/@id)
return
<div class="term">
    <dl class="term">
        <dt class="term">{ term:asLink($term) }</dt>
        <dd>
        { (: If any, display synonyms :)
            let $syns := term:synonyms($term)
            return
            if (exists($syns)) then
                <dl class="syn">
                    <dt class="in"><abbr class="small" title="[[ _('Synonyms') ]]">[[ _('syn.') ]]</abbr></dt>
                    <dd class="in">{
                        for $syn at $i in $syns
                        return
                            if ($i != count($syns)) then
                                ($syn, ", ")
                            else
                                $syn
                    }</dd>
                </dl>
            else ()
        }
            <dl class="trans">{ term:translations($term) }</dl>
        </dd>
    </dl>
    <ul class="termActions in hideme small weak">
        {{% if g.user %}}
        <li><a href="[[ url_for('terms.add', lang='{ $termLang }', term='{ $term/string() }') ]]">[[ _('Add synonym/translation') ]]</a></li>
        {{% endif %}}
        {{% if g.user.owns_term('{ $termID }') %}}
        <li><a href="[[ url_for('terms.edit', id='{ $termID }') ]]">[[ _('Edit term') ]]</a></li>
        {{% endif %}}

    </ul>
</div>
};
