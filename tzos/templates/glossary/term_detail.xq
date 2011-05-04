import module namespace tzos = "http://tzos.net/tzos" at "tzos.xqm";

for $term in collection($collection)//term
let $termLang := data($term/../../@xml:lang)
let $workingStatus := $term/../admin[@type="elementWorkingStatus"]/string()
where $term[starts-with(lower-case(string()), $letter)] and $term/../..[@xml:lang=$lang] and $workingStatus != "starterElement" and $workingStatus!="importedElement"
return
<div class="term">
    <dl class="term">
        <dt class="term">{ tzos:termLink($term) }</dt>
        <dd>
        { (: If any, display synonyms :)
            let $syns := tzos:getSynonyms($term)
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
            where $trans/../..[@xml:lang!=$lang]
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
