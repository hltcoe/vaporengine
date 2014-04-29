
function display_annotations(annotations){

    /*$.each(annotations,function(index,datum){
            console.log("---"+index);
            console.log(datum);
        });
    */
    
    $('#annotations_landing_zone').html(prettyPrint(annotations));
};

function display_utterances(utterances){
    $('#utterances_landing_zone').html(prettyPrint(utterances));
};

function display_pseudoterms(pseudoterms){
    $('#pseudoterms_landing_zone').html(prettyPrint(pseudoterms));
};

function display_audio_events(audio_events){
    $('#audio_events_landing_zone').html(prettyPrint(audio_events));
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


function get_utterances(){
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
            url: "http://localhost:12321/find_utterances",
                type: "POST",
                data: JSON.stringify(send),
                error: function(xhr, error) {
                alert('Error!  Status = ' + xhr.status + ' Message = ' + error);
            },
                success: function(data) {
                current_utterances = data;
                display_utterances(data);
            } 
        });
}


function get_audio_events(){

    send = {};
    send.dataset='buckeye' // HARDCODE
    send.count = 10; //TODO: pull from some element
    console.log(send)

    $.ajaxSetup({
            contentType: "application/json; charset=utf-8",
                dataType: "json"
                });

    $.ajax({
            url: "http://localhost:12321/find_audio_events",
                type: "POST",
                data: JSON.stringify(send),
                error: function(xhr, error) {
                alert('Error!  Status = ' + xhr.status + ' Message = ' + error);
            },
                success: function(data) {
                current_audio_events = data;
                display_audio_events(data);
            } 
        });
}


function get_pseudoterms(){

    send = {};
    send.dataset='buckeye' // HARDCODE
    send.count = 10; //TODO: pull from some element
    console.log(send)

    $.ajaxSetup({
            contentType: "application/json; charset=utf-8",
                dataType: "json"
                });

    $.ajax({
            url: "http://localhost:12321/find_pseudoterms",
                type: "POST",
                data: JSON.stringify(send),
                error: function(xhr, error) {
                alert('Error!  Status = ' + xhr.status + ' Message = ' + error);
            },
                success: function(data) {
                current_pseudoterms = data;
                display_pseudoterms(data);
            } 
        });
}




function test_ajax_calls(){
    get_annotation();
    get_utterances();
    get_audio_events();
    get_pseudoterms();
};


