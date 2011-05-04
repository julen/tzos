import module namespace tzos = "http://tzos.net/tzos" at "tzos.xqm";

let $term := collection($collection)//term[@id=$id]
return
<dl class="term">
    <dt class="term">{ $term/string() }</dt>
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

        <dl class="trans">
        {
        for $trans in $term/../../..//term
        let $transLang := data($trans/../../@xml:lang)
        let $termLang := data($term/../../@xml:lang)
        where $trans/../..[@xml:lang!=$termLang]
        return
        (
            <dt>{ $transLang }</dt>,
            <dd lang="{ $transLang }"><a href="[[ url_for('terms.detail', id='{ data($trans/@id) }') ]]">{ $trans/string() }</a></dd>
        )
        }
        </dl>
    </dd>
</dl>
