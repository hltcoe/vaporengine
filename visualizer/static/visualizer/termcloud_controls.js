var TermCloudControls = {
  addSizeControl: function(termCloud, default_size_key, size_keys) {
    termCloud.size_key = default_size_key;
    termCloud.size_keys = size_keys;

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

    $("#size_key_select").on('change', function(event) {
      var size_key = $("#size_key_select").val();
      termCloud.size_key = size_key;
      termCloud.render();
    });
  },

  addSortControl: function(termCloud, default_sort_key, sort_keys) {
    termCloud.collection.comparator = default_sort_key;
    termCloud.collection.sort();

    termCloud.sort_key = default_sort_key;
    termCloud.sort_keys = sort_keys;

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
                             function(event) {
                               var sort_key = $(this).val();
                               termCloud.collection.comparator = sort_key;
                               termCloud.collection.sort();
                               termCloud.render();
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
