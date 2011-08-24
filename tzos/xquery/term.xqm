module namespace term = "http://tzos.net/term";


(: Properties :)


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


declare function term:synonyms($tig as element(tig), $unreviewed as xs:boolean?) {
    let $synonyms :=
        for $syn in $tig/..//tig[data(@id) != $tig/data(@id)]
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


(: Main fields plus their updating counterparts :)

declare function term:term($tig as element(tig)) {
    $tig/term/string()
};

declare updating function term:term_update(
        $tig as element(tig),
        $term as xs:string) {
    (delete node $tig/term,
    insert node <term>{$term}</term> as first into $tig)
};


declare function term:concept_origin($tig as element(tig)) {
    string-join($tig/admin[@type="conceptOrigin"]/string(), ";;;")
};

declare updating function term:concept_origin_update(
        $tig as element(tig),
        $co_seq as xs:string*) {
    (delete node $tig/admin[@type="conceptOrigin"],
    for $co in $co_seq
        return insert node <admin type="conceptOrigin">{$co}</admin> into $tig)
};


declare function term:subject_field($tig as element(tig)) {
    string-join($tig/../../descrip[@type="subjectField"]/string(), ";;;")
};

declare updating function term:subject_field_update(
        $tig as element(tig),
        $sf_seq as xs:string*) {
    (delete node $tig/../../descrip[@type="subjectField"],
    for $sf in $sf_seq
        return insert node <descrip type="subjectField">{$sf}</descrip> into $tig/../..)
};


declare function term:working_status($tig as element(tig)) {
    $tig/admin[@type="elementWorkingStatus"]/string()
};

declare updating function term:working_status_update(
        $tig as element(tig),
        $ws as xs:string) {
    replace value of node $tig/admin[@type="elementWorkingStatus"] with $ws
};


declare function term:orig_person($tig as element(tig)) {
    string-join($tig/admin[@type="originatingPerson"]/string(), ";;;")
};

declare updating function term:orig_person_update(
        $tig as element(tig),
        $op_seq as xs:string*) {
    (delete node $tig/admin[@type="originatingPerson"],
    for $op in $op_seq
        return insert node <admin type="originatingPerson">{$op}</admin> into $tig)
};


declare function term:definition($tig as element(tig)) {
    string-join($tig/../descrip[@type="definition"]/string(), ";;;")
};

declare updating function term:definition_update(
        $tig as element(tig),
        $def_seq as xs:string*) {
    (delete node $tig/../descrip[@type="definition"],
    for $def in $def_seq
        return insert node <descrip type="definition">{$def}</descrip> into $tig/..)
};


declare function term:context($tig as element(tig)) {
    string-join($tig/descrip[@type="context"]/string(), ";;;")
};

declare updating function term:context_update(
        $tig as element(tig),
        $ctx_seq as xs:string*) {
    (delete node $tig/descrip[@type="context"],
    for $ctx in $ctx_seq
        return insert node <descrip type="context">{$ctx}</descrip> into $tig)
};


declare function term:example($tig as element(tig)) {
    string-join($tig/descrip[@type="example"]/string(), ";;;")
};

declare updating function term:example_update(
        $tig as element(tig),
        $ex_seq as xs:string*) {
    (delete node $tig/descrip[@type="example"],
    for $ex in $ex_seq
        return insert node <descrip type="example">{$ex}</descrip> into $tig)
};


declare function term:explanation($tig as element(tig)) {
    string-join($tig/descrip[@type="explanation"]/string(), ";;;")
};

declare updating function term:explanation_update(
        $tig as element(tig),
        $ex_seq as xs:string*) {
    (delete node $tig/descrip[@type="explanation"],
    for $ex in $ex_seq
        return insert node <descrip type="explanation">{$ex}</descrip> into $tig)
};


declare function term:entry_source($tig as element(tig)) {
    string-join($tig/admin[@type="entrySource"]/string(), ";;;")
};

declare updating function term:entry_source_update(
        $tig as element(tig),
        $es_seq as xs:string*) {
    (delete node $tig/admin[@type="entrySource"],
    for $es in $es_seq
        return insert node <admin type="entrySource">{$es}</admin> into $tig)
};


declare function term:product_subset($tig as element(tig)) {
    string-join($tig/admin[@type="productSubset"]/string(), ";;;")
};

declare updating function term:product_subset_update(
        $tig as element(tig),
        $ps_seq as xs:string*) {
    (delete node $tig/admin[@type="productSubset"],
    for $ps in $ps_seq
        return insert node <admin type="productSubset">{$ps}</admin> into $tig)
};


declare function term:subordinate_cg($tig as element(tig)) {
    string-join($tig/../../descrip[@type="subordinateConceptGeneric"]/string(), ";;;")
};

declare updating function term:subordinate_cg_update(
        $tig as element(tig),
        $scg_seq as xs:string*) {
    (delete node $tig/../../descrip[@type="subordinateConceptGeneric"],
    for $scg in $scg_seq
        return insert node <descrip type="subordinateConceptGeneric">{$scg}</descrip> into $tig/../..)
};


declare function term:superordinate_cg($tig as element(tig)) {
    string-join($tig/../../descrip[@type="superordinateConceptGeneric"]/string(), ";;;")
};

declare updating function term:superordinate_cg_update(
        $tig as element(tig),
        $scg_seq as xs:string*) {
    (delete node $tig/../../descrip[@type="superordinateConceptGeneric"],
    for $scg in $scg_seq
        return insert node <descrip type="superordinateConceptGeneric">{$scg}</descrip> into $tig/../..)
};


declare function term:antonym_concept($tig as element(tig)) {
    string-join($tig/../../descrip[@type="antonymConcept"]/string(), ";;;")
};

declare updating function term:antonym_concept_update(
        $tig as element(tig),
        $ac_seq as xs:string*) {
    (delete node $tig/../../descrip[@type="antonymConcept"],
    for $ac in $ac_seq
        return insert node <descrip type="antonymConcept">{$ac}</descrip> into $tig/../..)
};


declare function term:related_concept($tig as element(tig)) {
    string-join($tig/../../descrip[@type="relatedConcept"]/string(), ";;;")
};

declare updating function term:related_concept_update(
        $tig as element(tig),
        $rltd_seq as xs:string*) {
    (delete node $tig/../../descrip[@type="relatedConcept"],
    for $rltd in $rltd_seq
        return insert node <descrip type="relatedConcept">{$rltd}</descrip> into $tig/../..)
};


declare function term:pos($tig as element(tig)) {
    $tig/termNote[@type="partOfSpeech"]/string()
};

declare updating function term:pos_update(
        $tig as element(tig),
        $pos as xs:string) {
    replace value of node $tig/termNote[@type="partOfSpeech"] with $pos
};


declare function term:type($tig as element(tig)) {
    $tig/termNote[@type="termType"]/string()
};

declare updating function term:type_update(
        $tig as element(tig),
        $type as xs:string) {
    replace value of node $tig/termNote[@type="termType"] with $type
};


declare function term:admn_sts($tig as element(tig)) {
    $tig/termNote[@type="administrativeStatus"]/string()
};

declare updating function term:admn_sts_update(
        $tig as element(tig),
        $admn as xs:string) {
    replace value of node $tig/termNote[@type="administrativeStatus"] with $admn
};


declare function term:norm_auth($tig as element(tig)) {
    $tig/termNote[@type="normativeAuthorization"]/string()
};

declare function term:norm_auth_org($tig as element(tig)) {
    let $org := $tig/termNote[@type="normativeAuthorization"]/data(@target)
    return
        if (exists($org)) then
            $org
        else ("")
};

declare function term:norm_auth_org_display($tig as element(tig)) {
    let $nao := $tig/termNote[@type="normativeAuthorization"]/data(@target)
    let $org := collection($collection)//refObjectList[@type="respOrg"]/refObject[@id=$nao]/item[@type="org"]/string()
    return
        if (exists($org)) then
            $org
        else ("")
};

declare updating function term:norm_auth_update(
        $tig as element(tig),
        $na as xs:string,
        $na_org as xs:string) {

    replace value of node $tig/termNote[@type="normativeAuthorization"] with <termNote type="normativeAuthorization" target="{$na_org}">{$na}</termNote>
};


declare function term:xref($tig as element(tig)) {
    string-join($tig/ref[@type="crossReference"]/string(), ";;;")
};

declare updating function term:xref_update(
        $tig as element(tig),
        $xref_seq as xs:string*) {
    (delete node $tig/ref[@type="crossReference"],
    for $xref in $xref_seq
        return insert node <ref type="crossReference">{$xref}</ref> into $tig)
};


(: Methods :)

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
     term:norm_auth_org_display($tig),
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
