/** TermCloudControls - widgets for manipulating TermClouds
 *
 * There are two JS files for working with TermClouds - 'termcloud.js' and
 * 'termcloud_controls.js'.  The 'termcloud.js' file contains the Backbone.js
 * Model and View implementations.  The 'termcloud_controls.js' file implements
 * controls (buttons and menus) for manipulating TermClouds.  The control code
 * can "reach in" and manipulate TermCloud objects, but the TermCloud code
 * should not "reach out" (or depend on or have any awareness of) the control
 * code.
 *
 * Dependencies:
 *   Backbone.js
 *   jQuery
 *   Bootstrap    - TermCloud.render() uses Bootstrap tooltips
 */

/* globals termLabelText */

var TermCloudControls = {
  addAudioPlaybackEventHandler: function(termCloud, termVisualizer) {
    // Add event handler for when user clicks on item in TermCloud
    termCloud.on('click_model', function(model) {
      // Load and play audio file for this term
      termVisualizer.loadAndPlayURL('/visualizer/' + model.attributes.corpus_id + '/term/' + model.attributes.term_id + '.wav');
    });
  },

  addLabelEditorEventHandlers: function(termCloud) {
    function updateTermLabel() {
      var label = $('#term_label').val().trim();
      termCloud.activeTermCloudItemModel.attributes.label = label;
      termCloud.activeTermCloudItemModel.save();
      termCloud.collection.sort();
      $('#term_label_feedback').show();
      $('#term_label_feedback').delay(1000).fadeOut();
    }

    // Add event handler for when user clicks on item in TermCloud
    termCloud.on('click_model', function(model) {
      // Update text box for editing the label of the active term
      $('#term_label')
        .val(termLabelText(model.attributes));
    });

    // Add event handler when label in text box is updated
    $('#term_label').change(function() {
      updateTermLabel();
    });
  },

  addSizeControl: function(termCloud, default_size_key, size_keys) {
    termCloud.size_key = default_size_key;

    // Add size options to select control
    for (var i in size_keys) {
      $('#size_key_select').append(
        $('<option>')
          .text(size_keys[i].key_description)
          .val(size_keys[i].key_name));
    }

    $('#size_key_select').val(default_size_key);

    // Dynamically added select options won't be displayed until we issue 'refresh' command
    $('#size_key_select').selectpicker('refresh');

    $('#size_key_select').on('change', function(event) {
      var size_key = $('#size_key_select').val();
      termCloud.size_key = size_key;
      termCloud.updateFontSizeFunction();
      termCloud.render();
    });
  },

  addSortControl: function(termCloud, default_sort_key, sort_keys) {
    function getComparatorForSortKey(sortKey) {
      return function(a, b) {
        var a_attribute = a.attributes[sortKey];
        var b_attribute = b.attributes[sortKey];

        if ((a_attribute === '' || a_attribute === undefined) && b_attribute) {
          return 1;
        }
        else if (a_attribute && (b_attribute === '' || b_attribute === undefined)) {
          return -1;
        }
        else if (a_attribute < b_attribute) {
          return -1;
        }
        else if (a_attribute > b_attribute) {
          return 1;
        }
        else {
          return 0;
        }
      };
    }

    function getReverseComparatorForSortKey(sortKey) {
      return function(a, b) {
        var a_attribute = a.attributes[sortKey];
        var b_attribute = b.attributes[sortKey];

        if ((a_attribute === '' || a_attribute === undefined) && b_attribute) {
          return 1;
        }
        else if (a_attribute && (b_attribute === '' || b_attribute === undefined)) {
          return -1;
        }
        else if (a_attribute < b_attribute) {
          return 1;
        }
        else if (a_attribute > b_attribute) {
          return -1;
        }
        else {
          return 0;
        }
      };
    }

    function updateSortComparator() {
      var sort_key = $('#sort_key_select').val();

      if ($('#sort_direction').data('sort_reversed')) {
        termCloud.collection.comparator = getReverseComparatorForSortKey(sort_key);
      }
      else {
        termCloud.collection.comparator = getComparatorForSortKey(sort_key);
      }

      termCloud.collection.sort();
      termCloud.render();
    }

    $('#sort_direction').data('sort_reversed', true);
    termCloud.collection.comparator = getReverseComparatorForSortKey(default_sort_key);
    termCloud.collection.sort();

    termCloud.sort_keys = sort_keys;

    // Add sort options to select control
    for (var i in sort_keys) {
      $('#sort_key_select').append(
        $('<option>')
          .text(sort_keys[i].key_description)
          .val(sort_keys[i].key_name));
    }

    $('#sort_key_select').val(default_sort_key);

    // Dynamically added select options won't be displayed until we issue 'refresh' command
    $('#sort_key_select').selectpicker('refresh');

    $('#sort_key_select').on('change', updateSortComparator);

    $('#sort_direction').on('click',
                            function(event) {
                              if ($(this).data('sort_reversed')) {
                                $(this).data('sort_reversed', false);
                                $(this).removeClass('glyphicon-arrow-down');
                                $(this).addClass('glyphicon-arrow-up');
                              }
                              else {
                                $(this).data('sort_reversed', true);
                                $(this).removeClass('glyphicon-arrow-up');
                                $(this).addClass('glyphicon-arrow-down');
                              }
                              updateSortComparator();
                            });
  }
};


/** Adjust the padding at top of document
 */
function updateBodyPaddingTop() {
  if ($('#waveform_navbar').length > 0) {
    var new_control_height = 5 + $('#waveform_navbar').height();
    $('body').attr('style', 'padding-top: ' + new_control_height + 'px;');
  }
}
