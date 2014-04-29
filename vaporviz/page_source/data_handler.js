
function display_annotations(annotations){

    /*$.each(annotations,function(index,datum){
            console.log("---"+index);
            console.log(datum);
        });
    */
    
    $('#annotations_landing_zone').html(prettyPrint(annotations));
};

function get_annotation(){
    //dataset_name = $('#dataset_dropdown').val();

    send = {};
    send.dataset='buckeye' // HARDCODE
    send.count = 10; //TODO: pull from some element
    console.log(send)


    $.ajaxSetup({
            contentType: "application/json; charset=utf-8",
                dataType: "json"
                });

    $.ajax({
            url: "http://localhost:12321/find_annotations",
                type: "POST",
                data: JSON.stringify(send),
                error: function(xhr, error) {
                alert('Error!  Status = ' + xhr.status + ' Message = ' + error);
            },
                success: function(data) {
                current_annotations = data;
                display_annotations(data);
            } 
        });
}




function test_ajax_calls(){
    get_annotation();
};


