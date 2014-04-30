
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


function get_pseudoterm(pt_id){

    send = {};
    send.dataset='buckeye' // HARDCODE
    send.count = 1;
    send._id=(pt_id);
    

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
                active_pseudoterm = data[0]; //Global var
                $('#pt_eng_display')
                    .val(active_pseudoterm.eng_display);
                $('#pt_native_display')
                    .val(active_pseudoterm.native_display);
                $('#pt_stats_landing_zone')
                    .html(prettyPrint(active_pseudoterm));
                $('#pt_snippets_play_button')
                    .click(function(){playPseudoterm('pt_player', pt_id)});
                $('#pt_snippets_play_button')
                    .click(function(){playPseudoterm_with_context('pt_player', pt_id)});

                //Also get audioevents and snippets
            } 
        });
};
function get_pseudoterms(count){

    send = {};
    send.dataset='buckeye' // HARDCODE
    send.count = count || 10; //TODO: pull from some element

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
                //display_pseudoterms(data);
                active_pseudoterm = data[0]; //Global var
            } 
        });
};

function get_audio_events_from_pseudoterm(pseudoterm_id, count){

    send = {};
    send.dataset='buckeye'; //HARDCODE
    send.pt_id=pseudoterm_id;
    send.count= count || 10; //10 if nothing is specified in the call
    $.ajax({
            url: "http://localhost:12321/find_audio_events",
                type: "POST",
                data: JSON.stringify(send),
                error: function(xhr, error) {
                alert('Error!  Status = ' + xhr.status + ' Message = ' + error);
            },
                success: function(data) {
                display_audio_events(data)

            } 
        });
    

    
};


function annotate_pt_eng_label(){
    active_pt_id = active_pseudoterm._id;
    annotation = $('#pt_eng_display').val();
    send = {};
    send.dataset='buckeye'; //HARDCODE
    send._id=active_pt_id;
    send.eng_display = annotation;
    $.ajax({
            url: "http://localhost:12321/update_pseudoterm",
                type: "POST",
                data: JSON.stringify(send),
                error: function(xhr, error) {
                alert('Error!  Status = ' + xhr.status + ' Message = ' + error);
            },
                success: function(data) {
            } 
        });

};


function annotate_pt_native_label(){
    active_pt_id = active_pseudoterm._id;
    annotation = $('#pt_native_display').val();
    send = {};
    send.dataset='buckeye'; //HARDCODE
    send._id=active_pt_id;
    send.native_display = annotation;
    $.ajax({
            url: "http://localhost:12321/update_pseudoterm",
                type: "POST",
                data: JSON.stringify(send),
                error: function(xhr, error) {
                alert('Error!  Status = ' + xhr.status + ' Message = ' + error);
            },
                success: function(data) {
            } 
        });
    //Reload the PT now to see the changes reflected
    get_pseudoterm( active_pt_id );
    
};




function test_ajax_calls(){
    get_annotation();
    get_utterances();
    get_audio_events();
    get_pseudoterms();
};


