import module namespace term = "http://tzos.net/term" at "term.xqm";

for $term in collection($collection)//term
let $workingStatus := $term/../admin[@type="elementWorkingStatus"]/string()
where $term[starts-with(lower-case(string()), $letter)] and $term/../..[@xml:lang=$lang] and (term:is_public($term) or term:owner($term) = $current_user)
order by $term/string() ascending
return term:values($term)
