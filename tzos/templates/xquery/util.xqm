module namespace util = "http://tzos.net/util";


declare function util:join_seq($seq as element()*) {
    for $el at $i in $seq
    return
        if ($i != count($seq)) then
            ($el, ", ")
        else
            $el
};
