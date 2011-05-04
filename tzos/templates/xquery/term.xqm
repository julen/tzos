module namespace term = "http://tzos.net/term";


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


declare function term:display($term as element(term)) {
let $termLang := data($term/../../@xml:lang)
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
                    <dd class="in">{ string-join($syns, ", ") }</dd>
                </dl>
            else ()
        }
            <dl class="trans">{
            for $trans in $term/../../..//term
            let $transLang := data($trans/../../@xml:lang)
            where $trans/../..[@xml:lang!=$termLang]
            return
            (
                <dt>{ $transLang }</dt>,
                <dd lang="{ $transLang }"><a href="[[ url_for('terms.detail', id='{ data($trans/@id) }') ]]">{ $trans/string() }</a></dd>
            )}
            </dl>
        </dd>
    </dl>
    {{% if g.user %}}
    <ul class="termActions in hideme small weak">
        <li><a href="[[ url_for('terms.add', lang='{ $termLang }', term='{ $term/string() }') ]]">[[ _('Add synonym/translation') ]]</a></li>
    </ul>
    {{% endif %}}
</div>
};
