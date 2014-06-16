
// Functions declared in dynamic_wordclouds.js
/* global junk_displayed_token, make_me_a_venncloud, update_displayed_token  */

// GLOBAL VARIABLES declared in dynamic_wordclouds.js
/* global master_datasets, selected_datasets */

// Functions declared in third-party libraries
/* global prettyPrint */


var active_pseudoterm;
var cloud_datasets = [];


function get_cloud_data(corpus, utterance_list){

    var utterance_ids = utterance_list.utterance_ids;
    var dataset_name = utterance_list.dataset_name;

    return $.Deferred( function( defer ) {
        var send = {};
        send.dataset = corpus;
        send.utterances = utterance_ids;

        $.ajaxSetup({
            contentType: "application/json; charset=utf-8",
            dataType: "json"
        });

        $.ajax({
            url: "/cloud_data_from_utterances",
            type: "POST",
            data: JSON.stringify(send),
            error: function(xhr, error) {
                alert('Error!  Status = ' + xhr.status + ' Message = ' + error);
                defer.reject('Deferred error message');
            },
            success: function(data) {
                var wc_data = {};
                wc_data.dataset_name = dataset_name;
                wc_data.tokens = data;
                wc_data.num_tokens = data.length;
                wc_data.num_documents = utterance_ids.length;
                cloud_datasets.push(wc_data);
                defer.resolve(data);
            }
        });
    }).promise();
}


function get_pseudoterm(pt_id, corpus_name){
    var send = {};
    send.dataset=corpus_name;
    send.count = 1;
    send._id=(pt_id);

    $.ajaxSetup({
        contentType: "application/json; charset=utf-8",
        dataType: "json"
    });

    $.ajax({
        url: "/find_pseudoterms",
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
        }
    });
}


function annotate_pt_eng_label(corpus){
    var active_pt_id = active_pseudoterm._id;
    var annotation = $('#pt_eng_display').val();
    if (active_pseudoterm.eng_display === annotation){
        return;
    }
    else {
        var send = {};
        send.dataset=corpus;
        send._id=active_pt_id;
        send.eng_display = annotation;
        send.annotated = true;
        $.ajax({
            url: "/update_pseudoterm",
            type: "POST",
            data: JSON.stringify(send),
            error: function(xhr, error) {
                alert('Error!  Status = ' + xhr.status + ' Message = ' + error);
            },
            success: function(data) {
                get_pseudoterm(active_pt_id, corpus);
            }
        });
        update_displayed_token( active_pseudoterm.eng_display , annotation);
        set_active_wordcloud_token_by_text(annotation);
    }
}


function annotate_pt_native_label(corpus){
    var active_pt_id = active_pseudoterm._id;
    var annotation = $('#pt_native_display').val();
    var send = {};
    send.dataset=corpus;
    send._id=active_pt_id;
    send.native_display = annotation;
    $.ajax({
        url: "/update_pseudoterm",
        type: "POST",
        data: JSON.stringify(send),
        error: function(xhr, error) {
            alert('Error!  Status = ' + xhr.status + ' Message = ' + error);
        },
        success: function(data) {
            //Reload the PT now to see the changes reflected
            get_pseudoterm(active_pt_id, corpus);
        }
    });
}


function getURLforAudioEventWAV(corpus_name, audioEventID) {
    return '/corpus/' + corpus_name + '/audio/audio_event/' + audioEventID + '.wav';
}

function getURLforPseudotermWAV(corpus_name, pseudotermID) {
    return '/corpus/' + corpus_name +'/audio/pseudoterm/' + pseudotermID + '.wav';
}

function getURLforUtteranceWAV(corpus_name, utteranceID) {
    return '/corpus/' + corpus_name +'/audio/utterance/' + utteranceID + '.wav';
}


function junk_this_pseudoterm(event) {
    var active_pt_id = active_pseudoterm._id;
    var send = {};
    send.dataset = event.data.corpus;
    send._id=active_pt_id;
    $.ajax({
        url: "/junk_pseudoterm",
        type: "POST",
        data: JSON.stringify(send),
        error: function(xhr, error) {
            alert('Error!  Status = ' + xhr.status + ' Message = ' + error);
        }
    });

    junk_displayed_token( active_pseudoterm.eng_display );

    //Clear input fields for "English" and "Native" labels
    $("#pt_eng_display").val("");
    $("#pt_native_display").val("");

    if (event.data.waveform_visualizer) {
        event.data.waveform_visualizer.clear();
    }
}


function set_active_wordcloud_token_by_dom_id(token_dom_id) {
    // There can be only one
    $(".active_wordcloud_token").removeClass("active_wordcloud_token");
    $("#" + token_dom_id).addClass("active_wordcloud_token");
}


function set_active_wordcloud_token_by_text(token_text) {
    $("span.active_wordcloud_token").removeClass("active_wordcloud_token");

    $("span.wordcloud_token").each(function(index, element) {
        if (element.innerText === token_text) {
            element.classList.add("active_wordcloud_token");
        }
    });
}

/*
  set_up_annotate_pseudoterm_id() is a callback handler that is
  invoked when a user clicks on a word in a wordcloud.

  The callback function is assigned from make_me_a_venncloud() in
  Glen's dynamic_wordclouds.js.  The make_me_a_venncloud() function
  does not allow any parameters but 'token' to be passed to callback
  functions for words in the wordcloud - but we need to pass a 'corpus'
  parameter to set_up_annotate_pseudoterm_id().

  We use a constructor function to create a closure that allows
  set_up_annotate_pseudoterm_id() to access the 'corpus' parameter,
  without storing the 'corpus' parameter in a global variable.
*/
var CorpusClosureForSetupAnnotatePseudotermID = function(corpus, waveform_visualizer) {
    this.corpus = corpus;
    this.waveform_visualizer = waveform_visualizer;

    this.set_up_annotate_pseudoterm_id = function(token_text, token_element) {
        if (token_text.length > 50){ return; } //If you mistakenly click the whole box

        /*
        $.get('/www/pseudoterm_template.html',function(data){
            alert("in");
            $('#annotation_landing_zone').html(data);
            alert("Past");
        });
        */

        // master_datasets and selected_datasets are global variables defined in dynamic_wordclouds.js
        var token_container = master_datasets[selected_datasets[0]].tokens[token_text] ||
            master_datasets[selected_datasets[1]].tokens[token_text] ||
            [];
        var pt_ids = token_container.pt_ids;
        console.log(pt_ids);
        var pseudotermID = pt_ids[0];
        get_pseudoterm(pseudotermID, corpus); //Also posts to the global variable

        if (waveform_visualizer) {
            waveform_visualizer.loadAndPlayURL(getURLforPseudotermWAV(corpus, pseudotermID));
        }

        $("#pt_eng_display")
            .focusout(function(){
                annotate_pt_eng_label(corpus);
            })
            .keydown(function(e) {
                //Update annotation when users hit enter
                if (e.keyCode === 13) {
                    annotate_pt_eng_label(corpus);
                }
            });

        $("#pt_native_display")
            .focusout(function(){
                annotate_pt_native_label(corpus);
            });

        //Autoselect the english display element when user clicks on token
        $('#pt_eng_display').focus().select();

        set_active_wordcloud_token_by_dom_id(token_element.id);
    };
};

// Create a wordcloud (not a venncloud) from a single corpus of utterances
function wordcloud_from_utterances(corpus, utterances_list, waveform_visualizer, options){
    var corpus_closure = new CorpusClosureForSetupAnnotatePseudotermID(corpus, waveform_visualizer);

    if (options === undefined) {
        options = {};
    }
    options.click = corpus_closure.set_up_annotate_pseudoterm_id;

    $.when(get_cloud_data(corpus, utterances_list[0])).done( function(){
        var
          dataset,
          i,
          token,
          token_name;

        // Add class names for audio events, pseudoterms, utterances to token.span_classes
        dataset = cloud_datasets[0];
        for (token_name in dataset.tokens) {
            token = dataset.tokens[token_name];
            token.span_classes = ['wordcloud_token'];
            for (i = 0; i < token.audio_event_ids.length; i++) {
                token.span_classes.push("audio_event_span_" + token.audio_event_ids[i]);
            }
            for (i = 0; i < token.pt_ids.length; i++) {
                token.span_classes.push("pseudoterm_span_" + token.pt_ids[i]);
            }
            for (i = 0; i < token.utterance_ids.length; i++) {
                token.span_classes.push("utterance_span_" + token.utterance_ids[i]);
            }
        }
        make_me_a_venncloud( cloud_datasets, options );
    });
}

function venncloud_from_utterances(corpus, utterances_lists, waveform_visualizer, options){
    var corpus_closure = new CorpusClosureForSetupAnnotatePseudotermID(corpus, waveform_visualizer);

    if (options === undefined) {
        options = {};
    }
    options.click = corpus_closure.set_up_annotate_pseudoterm_id;

    var u = utterances_lists;
    $.when(get_cloud_data(corpus, u[0] ), get_cloud_data(corpus, u[1] )).done( function(){
        make_me_a_venncloud( cloud_datasets, options );
    });
}
