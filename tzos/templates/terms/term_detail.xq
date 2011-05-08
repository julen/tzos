import module namespace term = "http://tzos.net/term" at "term.xqm";

for $term in collection($collection)//term[@id=$id]
where term:owner($term) = $current_user or term:is_public($term)
return term:display($term)
