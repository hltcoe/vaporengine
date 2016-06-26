// There is *extensive* coupling between this JavaScript file, the
// controller, and the views.  The JavaScript code assumes that DOM
// elements with certain ID's exist.  The code also assumes that
// controller URLs both exist and will return data in an expected
// format.


/** Add event handlers for when user changes the label for a term
 */
function addLabelEditorEventHandlers() {
  $("#term_label")
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


function addSizeControl(wordcloud_div_id, default_size_key, size_keys) {
  // Add size options to select control
  for (var i in size_keys) {
    $("#size_key_select").append(
      $('<option>')
        .text(size_keys[i].key_description)
        .val(size_keys[i].key_name));
  }

  $("#size_key_select").val(default_size_key);

  // Dynamically added select options won't be displayed until we issue 'refresh' command
  $("#size_key_select").selectpicker('refresh');
  $("#size_key_select").on('change',
                           {'selector': '#'+wordcloud_div_id+'>span.wordcloud_token'},
                           function(event) {
                             var size_key = $("#size_key_select").val();
                             $(event.data.selector).each(function() {
                               var term = $(this).data('term');
                               $(this).css('font-size', Math.sqrt(term[size_key]) + 'em');
                             });
                           });
}


function addSortControl(wordcloud_div_id, default_sort_key, sort_keys) {
  // Add sort options to select control
  for (var i in sort_keys) {
    $("#sort_key_select").append(
      $('<option>')
        .text(sort_keys[i].key_description)
        .val(sort_keys[i].key_name));
  }

  $("#sort_key_select").val(default_sort_key);

  // Dynamically added select options won't be displayed until we issue 'refresh' command
  $("#sort_key_select").selectpicker('refresh');
  $("#sort_key_select").on('change',
                           {'selector': '#'+wordcloud_div_id+'>span'},
                           function(event) {
                             sortDOMElementsByDataField(event.data.selector, $(this).val());
                           });


  // Add sort options to drop-down menu
  for (var i in sort_keys) {
    $("#sort_menu_items").append(
      $('<li>')
        .html('<a href="#">' + sort_keys[i].key_description + '</a>')
        .on('click',
            {'dataSortField': sort_keys[i].key_name, 'selector': '#'+wordcloud_div_id+'>span'},
            function(event) {
              sortDOMElementsByDataField(event.data.selector, event.data.dataSortField);
            })
    );
  }
}



/**
 *
 */
function createWordcloud(wordcloud_div_id, json_term_data_url, termVisualizer) {
  $.getJSON(json_term_data_url, function(data) {
    var default_size_key = data.default_size_key;
    var default_sort_key = data.default_sort_key;
    var size_keys = data.size_keys;
    var sort_keys = data.sort_keys;
    var terms = data.terms;
    var wordcloud_div = $("#" + wordcloud_div_id);

    addSizeControl(wordcloud_div_id, default_size_key, size_keys);
    addSortControl(wordcloud_div_id, default_sort_key, sort_keys);

    for (var termIndex in terms) {
      var term = terms[termIndex];

      // Create <span> for term
      var term_span = $('<span>')
        .attr('id', 'term_' + term.term_id)
        .on('click',
            {'corpus_id': term.corpus_id, 'term_id': term.term_id, 'termVisualizer': termVisualizer},
            updateActiveTerm);

      // Add term data to <span> for term
      term_span.data('term', term);
      for (var key in term) {
        if (term.hasOwnProperty(key)) {
          term_span.data(key, term[key]);
        }
      }

      // Adjust font size
      term_span.css('font-size', Math.sqrt(term[default_size_key]) + 'em');

      // Add CSS classes to <span> for term
      var span_classes = ['wordcloud_token'];
      for (var i = 0; i < term.audio_fragment_ids.length; i++) {
        span_classes.push("audio_fragment_span_" + term.audio_fragment_ids[i]);
      }
      term_span.addClass(span_classes.join(" "));

      // Add tooltip to <span> for term
      var tooltip_text = "";
      for (var i in sort_keys) {
        tooltip_text += sort_keys[i].key_description + ": " + term[sort_keys[i].key_name] + "\n";
      }
      term_span
        .attr('data-placement', 'bottom')
        .attr('data-toggle', 'tooltip')
        .attr('title', tooltip_text)
        .tooltip();

      term_span.text(termLabelText(term));
      wordcloud_div.append(term_span);
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
 * @param {String} dataSortField - Name of data field to sort by
 * @param {String} selector - CSS selector
 */
function sortDOMElementsByDataField(selector, dataSortField) {
  tinysort(selector, {sortFunction: function(a, b) {
    return ($(a.elm).data(dataSortField)) > ($(b.elm).data(dataSortField)) ? 1 : -1;
  }});
}


function termLabelText(term) {
  if (term.label) {
    return term.label;
  }
  else {
    return "T" + term.zr_term_index;
  }
}


/**
 * @param {Event} event - An Event object with data fields corpus_id, term_id, termVisualizer
 */
function updateActiveTerm(event) {
  var corpus_id = event.data.corpus_id;
  var term_id = event.data.term_id;
  var termVisualizer = event.data.termVisualizer;
  var term = $("#term_" + term_id).data('term')

  // Update text box for editing the label of the active term
  $('#term_label')
    .data('term_id', term_id)
    .val(termLabelText(term));

  // There can be only one active term at a time
  $(".active_wordcloud_token").removeClass("active_wordcloud_token");
  $("#term_" + term_id).addClass("active_wordcloud_token");

  // Load and play audio file for this term
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
  var term_id = $("#term_label").data('term_id');

  // Only update the term label if the user has previously selected a term
  if (term_id) {
    var label = $("#term_label").val().trim();
    var term = $("#term_" + term_id).data("term");
    term.label = label;

    $("#term_" + term_id)
      // Update the term data attached to DOM element for the wordcloud term
      .data("term", term)
      // Update the term label shown in the word cloud
      .text(termLabelText(term));

    $.ajax({
      url: "/visualizer/term/"+term_id+"/update",
      type: "POST",
      data: JSON.stringify({
        "label": label
      })
    });
  }
}
