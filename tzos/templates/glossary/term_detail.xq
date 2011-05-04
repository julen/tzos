import module namespace term = "http://tzos.net/term" at "term.xqm";

for $term in collection($collection)//term
let $workingStatus := $term/../admin[@type="elementWorkingStatus"]/string()
where $term[starts-with(lower-case(string()), $letter)] and $term/../..[@xml:lang=$lang] and $workingStatus != "starterElement" and $workingStatus!="importedElement"
return term:display($term)
