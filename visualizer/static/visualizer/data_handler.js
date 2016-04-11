
// Functions declared in dynamic_wordclouds.js
/* global junk_displayed_token, make_me_a_venncloud, update_displayed_token  */

// GLOBAL VARIABLES declared in dynamic_wordclouds.js
/* global master_datasets, selected_datasets */

// Functions declared in third-party libraries
/* global prettyPrint */


var active_pseudoterm;
var cloud_datasets = [];


/**
 * @param {String} corpus_name
 * @param {Array} utterance_list
 */
function get_cloud_data(corpus_id, utterance_list){

    var utterance_ids = utterance_list.utterance_ids;
    var dataset_name = utterance_list.dataset_name;

    return $.Deferred( function( defer ) {
        var send = {};
        send.dataset = corpus_id;
        send.utterances = utterance_ids;

        $.ajaxSetup({
            contentType: "application/json; charset=utf-8",
            dataType: "json"
        });

        $.ajax({
            url: "/venncloud_json_for_document",
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


function get_corpus_venncloud_data(corpus_id) {
    return $.Deferred( function( defer ) {
        var send = {};
        send.corpus_id = corpus_id;

        $.ajaxSetup({
            contentType: "application/json; charset=utf-8",
            dataType: "json"
        });

        $.ajax({
            url: "/visualizer/venncloud_json_for_corpus",
            type: "POST",
            data: JSON.stringify(send),
            error: function(xhr, error) {
                alert('Error!  Status = ' + xhr.status + ' Message = ' + error);
                defer.reject('Deferred error message');
            },
            success: function(data) {
                var wc_data = {};
                wc_data.dataset_name = "Ignored";
                wc_data.tokens = data;
                wc_data.num_tokens = data.length;
                wc_data.num_documents = 1; // utterance_ids.length;
                cloud_datasets.push(wc_data);
                defer.resolve(data);
            }
        });
    }).promise();
}


/**
 * @param {Integer} term_id
 * @param {Integer} corpus_id
 */
function get_pseudoterm(term_id, corpus_id){
    var send = {};
    send.corpus_id=corpus_id;
    send.term_id=term_id;

    $.ajaxSetup({
        contentType: "application/json; charset=utf-8",
        dataType: "json"
    });

    $.ajax({
        url: "/visualizer/"+corpus_id+"/term/"+term_id+".json",
        type: "POST",
        data: JSON.stringify(send),
        error: function(xhr, error) {
            alert('Error!  Status = ' + xhr.status + ' Message = ' + error);
        },
        success: function(data) {
            active_pseudoterm = data; //Global var
            $('#pt_eng_display')
                .val(active_pseudoterm.eng_display);
            $('#pt_native_display')
                .val(active_pseudoterm.native_display);
            $('#pt_stats_landing_zone')
                .html(prettyPrint(active_pseudoterm));
        }
    });
}


/**
 * @param {String} corpus_name
 */
function annotate_pt_eng_label(corpus_name){
    var active_pt_id = active_pseudoterm._id;
    var annotation = $('#pt_eng_display').val();
    if (active_pseudoterm.eng_display === annotation){
        return;
    }
    else {
        var send = {};
        send.dataset=corpus_name;
        send._id=active_pt_id;
        send.eng_display = annotation;
        send.annotated = true;
        $.ajax({
            url: "/visualizer/"+corpus_name+"/term/"+active_pt_id+"/update",
            type: "POST",
            data: JSON.stringify(send),
            error: function(xhr, error) {
                alert('Error!  Status = ' + xhr.status + ' Message = ' + error);
            },
            success: function(data) {
                get_pseudoterm(active_pt_id, corpus_name);
            }
        });
        update_displayed_token( active_pseudoterm.eng_display , annotation);
        set_active_wordcloud_token_by_text(annotation);
    }
}


/**
 * @param {String} corpus_name
 */
function annotate_pt_native_label(corpus_name){
    var active_pt_id = active_pseudoterm._id;
    var annotation = $('#pt_native_display').val();
    var send = {};
    send.dataset=corpus_name;
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
            get_pseudoterm(active_pt_id, corpus_name);
        }
    });
}


/**
 * @param {String} corpus_name
 * @param {String} audioEventID
 */
function getURLforAudioEventWAV(corpus_name, audioEventID) {
    return '/corpus/' + corpus_name + '/audio/audio_event/' + audioEventID + '.wav';
}

/**
 * @param {Integer} corpus_id
 * @param {String} audioEventID
 */
function getURLforPseudotermWAV(corpus_id, term_id) {
    return '/visualizer/' + corpus_id +'/term/' + term_id + '.wav';
}

/**
 * @param {String} corpus_name
 * @param {String} audioEventID
 */
function getURLforUtteranceWAV(corpus_name, utteranceID) {
    return '/corpus/' + corpus_name +'/audio/utterance/' + utteranceID + '.wav';
}


/**
 * @callback
 * @param {MouseEvent} event
 */
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


/**
 * @param {String} token_dom_id
 */
function set_active_wordcloud_token_by_dom_id(token_dom_id) {
    // There can be only one
    $(".active_wordcloud_token").removeClass("active_wordcloud_token");
    $("#" + token_dom_id).addClass("active_wordcloud_token");
}


/**
 * @param {String} token_text
 */
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
  functions for words in the wordcloud - but we need to pass a 'corpus_name'
  parameter to set_up_annotate_pseudoterm_id().

  We use a constructor function to create a closure that allows
  set_up_annotate_pseudoterm_id() to access the 'corpus_name' parameter,
  without storing the 'corpus_name' parameter in a global variable.
*/
/**
 * @param {Integer} corpus_id
 * @param {WaveformVisualizer} waveform_visualizer
 */
var CorpusClosureForSetupAnnotatePseudotermID = function(corpus_id, waveform_visualizer) {
    this.corpus_id = corpus_id;
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
        get_pseudoterm(pseudotermID, corpus_id); //Also posts to the global variable

        if (waveform_visualizer) {
            waveform_visualizer.loadAndPlayURL(getURLforPseudotermWAV(corpus_id, pseudotermID));
        }

        $("#pt_eng_display")
            .focusout(function(){
                annotate_pt_eng_label(corpus_id);
            })
            .keydown(function(e) {
                //Update annotation when users hit enter
                if (e.keyCode === 13) {
                    annotate_pt_eng_label(corpus_id);
                }
            });

        $("#pt_native_display")
            .focusout(function(){
                annotate_pt_native_label(corpus_id);
            });

        //Autoselect the english display element when user clicks on token
        $('#pt_eng_display').focus().select();

        set_active_wordcloud_token_by_dom_id(token_element.id);
    };
};

/** Create a wordcloud (not a venncloud) for all Terms in a corpus
 * @param {Integer} corpus_id
 * @param {WaveformVisualizer} waveform_visualizer
 * @param {Object} options
 */
function wordcloud_from_corpus(corpus_id, waveform_visualizer, options) {
    var corpus_closure = new CorpusClosureForSetupAnnotatePseudotermID(corpus_id, waveform_visualizer);

    if (options === undefined) {
        options = {};
    }
    options.click = corpus_closure.set_up_annotate_pseudoterm_id;

    $.when(get_corpus_venncloud_data(corpus_id)).done( function(){
        var
          dataset,
          i,
          token,
          token_text;

        // Add class names for audio events, pseudoterms, utterances to token.span_classes
        dataset = cloud_datasets[0];
        for (token_text in dataset.tokens) {
            token = dataset.tokens[token_text];
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


/** Create a wordcloud (not a venncloud) from a single set of utterances
 * @param {Integer} corpus_id
 * @param {Array} utterances_list
 * @param {WaveformVisualizer} waveform_visualizer
 * @param {Object} options
 */
function wordcloud_from_utterances(corpus_id, utterances_list, waveform_visualizer, options){
    var corpus_closure = new CorpusClosureForSetupAnnotatePseudotermID(corpus_id, waveform_visualizer);

    if (options === undefined) {
        options = {};
    }
    options.click = corpus_closure.set_up_annotate_pseudoterm_id;

    $.when(get_cloud_data(corpus_id, utterances_list[0])).done( function(){
        var
          dataset,
          i,
          token,
          token_text;

        // Add class names for audio events, pseudoterms, utterances to token.span_classes
        dataset = cloud_datasets[0];
        for (token_text in dataset.tokens) {
            token = dataset.tokens[token_text];
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

/**
 * @param {Integer} corpus_id
 * @param {Array} utterances_lists
 * @param {WaveformVisualizer} waveform_visualizer
 * @param {Object} options
 */
/*
function venncloud_from_utterances(corpus_id, utterances_lists, waveform_visualizer, options){
    var corpus_closure = new CorpusClosureForSetupAnnotatePseudotermID(corpus_id, waveform_visualizer);

    if (options === undefined) {
        options = {};
    }
    options.click = corpus_closure.set_up_annotate_pseudoterm_id;

    var u = utterances_lists;
    $.when(get_cloud_data(corpus_id, u[0] ), get_cloud_data(corpus_id, u[1] )).done( function(){
        make_me_a_venncloud( cloud_datasets, options );
    });
}
*/
