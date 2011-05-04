import module namespace term = "http://tzos.net/term" at "term.xqm";

let $term := collection($collection)//term[@id=$id]
return  term:display($term)
