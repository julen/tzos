import module namespace term = "http://tzos.net/term" at "term.xqm";

for $term in collection($collection)//term
where dbxml:contains($term/string(), $q) and term:is_public($term)
return term:asLink($term)
