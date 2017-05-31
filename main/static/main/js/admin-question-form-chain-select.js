window.onload = function(){

    function newParameters(query) {
            query.category = grp.jQuery("#id_category").val();
        }
        grp.jQuery('#id_topic_0').djselectable('option', 'prepareQuery', newParameters);
}