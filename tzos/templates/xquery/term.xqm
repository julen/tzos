module namespace tzos = "http://tzos.net/tzos";


declare function tzos:termLink($term as element(term))
as element(a) {
    <a href="[[ url_for('terms.detail', id='{ data($term/@id) }') ]]">{ $term/string() }</a>
};


declare function tzos:getSynonyms($term as element(term)) {
    for $syn in $term/../..//term[string()!=$term/string()]
    let $workingStatus := $syn/../admin[@type="elementWorkingStatus"]/string()
    where $workingStatus != "starterElement" and $workingStatus != "importedElement"
    return tzos:termLink($syn)
};
