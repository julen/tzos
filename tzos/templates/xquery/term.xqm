module namespace term = "http://tzos.net/term";

import module namespace util = "http://tzos.net/util" at "util.xqm";


declare function term:owner($tig as element(tig))
{
    $tig/transacGrp[./transac[@type="transactionType"]/string()="origination" or ./transac[@type="transactionType"]/string()="input" or ./transac[@type="transactionType"]/string()="importation"]/transacNote[@type="responsibility"]/string()
};

declare function term:sortkey($tig as element(tig))
{
    $tig/admin[@type="sortKey"]/string()
};

declare function term:lock($tig as element(tig))
{
    $tig/@lock
};

declare function term:is_public($tig as element(tig))
as xs:boolean {
let $workingStatus := term:working_status($tig)
return $workingStatus != "starterElement" and $workingStatus != "importedElement" and $workingStatus != "archiveElement"
};

declare function term:is_unreviewed($tig as element(tig))
as xs:boolean {
let $workingStatus := term:working_status($tig)
return $workingStatus = "starterElement" or $workingStatus = "importedElement"
};

declare function term:term($tig as element(tig)) {
    $tig/term/string()
};


declare function term:synonyms($tig as element(tig), $unreviewed as xs:boolean?) {
    let $synonyms :=
        for $syn in $tig/..//tig[term/string() != term:term($tig)]
        let $synID := $syn/data(@id)
        where (if ($unreviewed) then true() else term:is_public($syn))
        return string-join(($synID, term:term($syn)), ";")
    return string-join($synonyms, ";;;")
};


declare function term:translations($tig as element(tig), $unreviewed as xs:boolean?)
{
    let $translations :=
        for $trans in $tig/../..//tig
        let $transID := $trans/data(@id)
        let $termLang := data($tig/../@xml:lang)
        let $transLang := data($trans/../@xml:lang)
        let $workingStatus := term:working_status($trans)
        where $trans/..[@xml:lang!=$termLang] and
            (if ($unreviewed) then true() else term:is_public($trans))
        return string-join(($transLang, $transID, term:term($trans)), ";")
    return string-join($translations, ";;;")
};


declare function term:type($tig as element(tig)) {
    $tig/termNote[@type="termType"]/string()
};


declare function term:pos($tig as element(tig)) {
    $tig/termNote[@type="partOfSpeech"]/string()
};


declare function term:admn_sts($tig as element(tig)) {
    $tig/termNote[@type="administrativeStatus"]/string()
};


declare function term:norm_auth($tig as element(tig)) {
    $tig/termNote[@type="normativeAuthorization"]/string()
};


declare function term:norm_auth_org($tig as element(tig)) {
    let $nao := $tig/termNote[@type="normativeAuthorization"]/data(@target)
    let $org := collection($collection)//refObjectList[@type="respOrg"]/refObject[@id=$nao]/item[@type="org"]/string()
    return
        if (exists($org)) then
            $org
        else ("")
};


declare function term:concept_origin($tig as element(tig)) {
    string-join($tig/admin[@type="conceptOrigin"]/string(), ";;;")
};


declare function term:orig_person($tig as element(tig)) {
    string-join($tig/admin[@type="originatingPerson"]/string(), ";;;")
};


declare function term:product_subset($tig as element(tig)) {
    $tig/admin[@type="productSubset"]/string()
};


declare function term:working_status($tig as element(tig)) {
    $tig/admin[@type="elementWorkingStatus"]/string()
};


declare function term:entry_source($tig as element(tig)) {
    $tig/admin[@type="entrySource"]/string()
};


declare function term:subject_field($tig as element(tig)) {
    string-join($tig/../../descrip[@type="subjectField"]/string(), ";;;")
};


declare function term:subordinate_cg($tig as element(tig)) {
    $tig/../../descrip[@type="subordinateConceptGeneric"]/string()
};


declare function term:superordinate_cg($tig as element(tig)) {
    $tig/../../descrip[@type="superordinateConceptGeneric"]/string()
};


declare function term:antonym_concept($tig as element(tig)) {
    $tig/../../descrip[@type="antonymConcept"]/string()
};


declare function term:related_concept($tig as element(tig)) {
    $tig/../../descrip[@type="relatedConcept"]/string()
};


declare function term:definition($tig as element(tig)) {
    $tig/../descrip[@type="definition"]/string()
};


declare function term:context($tig as element(tig)) {
    $tig/descrip[@type="context"]/string()
};


declare function term:example($tig as element(tig)) {
    $tig/descrip[@type="example"]/string()
};


declare function term:explanation($tig as element(tig)) {
    $tig/descrip[@type="explanation"]/string()
};


declare function term:xref($tig as element(tig)) {
    $tig/ref[@type="crossReference"]/string()
};

declare function term:xref_id($tig as element(tig)) {
    $tig/ref[@type="crossReference"]/data(@target)
};


declare function term:activity($tx as element(transacGrp)) {
string-join(
    ($tx/../data(@id),
     $tx/../term/string(),
     $tx/transac[@type="transactionType"]/string(),
     $tx/date/string(),
     $tx/transacNote[@type="responsibility"]/string()
     ), "|||")
};


declare function term:values($tig as element(tig), $unreviewed as xs:boolean?) {
string-join(
    ($tig/data(@id), (: term ID :)
     $tig/../data(@xml:lang), (: language of the term :)
     term:term($tig),
     term:concept_origin($tig),
     term:subject_field($tig),
     term:orig_person($tig),
     term:definition($tig),
     term:context($tig),
     term:example($tig),
     term:explanation($tig),
     term:entry_source($tig),
     term:xref($tig),
     term:product_subset($tig),
     term:norm_auth($tig),
     term:norm_auth_org($tig),
     term:subordinate_cg($tig),
     term:superordinate_cg($tig),
     term:antonym_concept($tig),
     term:related_concept($tig),
     term:pos($tig),
     term:type($tig),
     term:admn_sts($tig),
     term:synonyms($tig, $unreviewed),
     term:translations($tig, $unreviewed),
     term:working_status($tig),
     term:owner($tig),
     term:sortkey($tig),
     term:lock($tig)
     ), "|||")
};
