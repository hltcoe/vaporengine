/** Add event handlers for when user changes the label for a term
 */
function addLabelEditorEventHandlers() {
  $("#pt_eng_display")
    .focusout(function() {
      updateTermLabel();
    })
    .keydown(function(e) {
      // Update annotation when users hit enter
      if (e.keyCode === 13) {
        updateTermLabel();
      }
    });
}


/**
 *
 */
function createWordcloud(wordcloud_div_id, json_term_data_url, termVisualizer) {
  $.getJSON(json_term_data_url, function(data) {
    var sort_keys = data.sort_keys;
    var terms = data.terms;
    var wordcloud_div = $("#" + wordcloud_div_id);

    // Add sort options
/*
    for (var key in sort_keys) {
      $("#sort_key_select").append(
        $('<option>')
          .text(sort_keys[key])
          .val(key));
    }

    // Dynamically added select options won't be displayed until we issue 'refresh' command
    $("#sort_key_select").selectpicker('refresh');

    $("#sort_key_select").on('change', function(event) {
      var sort_type = $(this).val();
      tinysort("#wordcloud_div>span", {sortFunction: function(a, b) {
        return ($(a.elm).data(sort_type)) > ($(b.elm).data(sort_type)) ? 1 : -1;
      }})
    });
*/

    for (var key in sort_keys) {
      $("#sort_menu_items").append(
        $('<li>')
          .html('<a href="#">' + sort_keys[key] + '</a>')
          .on('click',
              {'dataSortField': key, 'selector': '#'+wordcloud_div_id+'>span'},
              sortDOMElementsByDataField));
    }

    for (var termIndex in terms) {
      var i;
      var term = terms[termIndex];
      var tooltip_text = "";

      var wordcloud_span = $('<span>')
        .attr('id', 'term_' + term.term_id)
        .on('click',
            {'corpus_id': term.corpus_id, 'term_id': term.term_id, 'termVisualizer': termVisualizer},
            updateActiveTerm);

      $.each(term, function(key, value) {
        wordcloud_span.data(key, value);
        if (sort_keys[key]) {
          tooltip_text += sort_keys[key] + ": " + value + "\n";
        }
      });

      var span_classes = ['wordcloud_token'];
      for (i = 0; i < term.audio_event_ids.length; i++) {
        span_classes.push("audio_event_span_" + term.audio_event_ids[i]);
      }
      wordcloud_span.addClass(span_classes.join(" "));

      // Add tooltip
      wordcloud_span
        .attr('data-placement', 'bottom')
        .attr('data-toggle', 'tooltip')
        .attr('title', tooltip_text)
        .tooltip();

      wordcloud_span.text(term.eng_display);
      wordcloud_div.append(wordcloud_span);
    }
  });
}


/** Uses TinySort to sort DOM elements based on specified data field
 *
 * The TinySort script (http://tinysort.sjeiti.com) nominally has
 * support for sorting DOM elements by data fields using the syntax:
 *   tinysort(selector, {data: dataSortField});
 * but this syntax does not work for data fields that have been set using
 * jQuery's data() function.  For more details about the way that $.data
 * behaves vs. $.attr when accessing data-someAttribute, see this
 * StackOverflow post:
 *   http://stackoverflow.com/questions/7261619/jquery-data-vs-attr
 *
 * @param {Event} event - An Event object with data fields dataSortField and selector
 */
function sortDOMElementsByDataField(event) {
  var dataSortField = event.data.dataSortField;
  var selector = event.data.selector;
  tinysort(selector, {sortFunction: function(a, b) {
    return ($(a.elm).data(dataSortField)) > ($(b.elm).data(dataSortField)) ? 1 : -1;
  }});
}


/**
 *
 */
function updateActiveTerm(event) {
  var corpus_id = event.data.corpus_id;
  var term_id = event.data.term_id;
  var termVisualizer = event.data.termVisualizer;

  $('#pt_eng_display')
    .data('term_id', term_id)
    .val($("#term_" + term_id).data("eng_display"));

  // There can be only one active term at a time
  $(".active_wordcloud_token").removeClass("active_wordcloud_token");
  $("#term_" + term_id).addClass("active_wordcloud_token");

  termVisualizer.loadAndPlayURL('/visualizer/' + corpus_id + '/term/' + term_id + '.wav');
}


/** Adjust the padding at top of document when height of navbar changes
 */
function updateBodyPaddingWhenControlsChangeSize() {
  if ($('#waveform_navbar').length > 0) {
    var new_control_height = 5 + $('#waveform_navbar').height();
    $('body').attr('style', 'padding-top: ' + new_control_height + 'px;');
  }
}


function updateTermLabel() {
  var label = $("#pt_eng_display").val();
  var term_id = $("#pt_eng_display").data('term_id');

  // Only update the term label if the user has previously selected a term
  if (term_id) {
    $("#term_" + term_id)
      // Store the label field as data attached to DOM element for the wordcloud word
      .data("eng_display", label)
      // Update the term label shown in the word cloud
      .text(label);

    $.ajax({
      url: "/visualizer/term/"+term_id+"/update",
      type: "POST",
      data: JSON.stringify({
        "eng_display": label
      })
    });
  }
}
