import module namespace term = "http://tzos.net/term" at "term.xqm";

let $term := collection($collection)//term[@id=$id]
let $workingStatus := $term/../admin[@type="elementWorkingStatus"]/string()
where $workingStatus != "starterElement" and $workingStatus!="importedElement"
return term:display($term)
