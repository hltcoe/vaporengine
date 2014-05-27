<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="/static/jquery-ui-1.10.4/css/ui-lightness/jquery-ui-1.10.4.css"/>
  <link rel="stylesheet" href="/static/bootstrap-3.1.1/css/bootstrap.css"/>
  <link rel="stylesheet" href="/static/bootstrap-3.1.1/css/bootstrap-theme.css"/>

  <link rel="stylesheet" href="/www/dynamic_wordclouds.css"/>

  <script src="/static/jquery-1.11.0.min.js"></script>
  <script src="/static/jquery-ui-1.10.4/js/jquery-ui-1.10.4.min.js"></script>
  <script src="/static/bootstrap-3.1.1/js/bootstrap.js"></script>

  <script src="/www/floating-1.12.js"></script>
  <script src="/www/dynamic_wordclouds.js"></script>
  <script src="/www/prettyprint.js"></script>

  <script src="/static/wavesurfer/wavesurfer.js"></script>
  <script src="/static/wavesurfer/webaudio.js"></script>
  <script src="/static/wavesurfer/webaudio.buffer.js"></script>
  <script src="/static/wavesurfer/webaudio.media.js"></script>
  <script src="/static/wavesurfer/drawer.js"></script>
  <script src="/static/wavesurfer/drawer.canvas.js"></script>

  <script src="/www/vapor_audio.js"></script>
  <script src="/www/data_handler.js"></script>

  <style>
    /* Hide drop-down boxes for selecting Left and Right datasets */
    #wordcloud_landing_zone thead {
      display: none;
    }
  </style>

  <script>
    $(document).ready(function() {
      var waveformVisualizer = new WaveformVisualizer('waveform_visualizer');
      waveformVisualizer.addControls($('#pt_snippets_audio_player'));

      var utterance_set1 = {
        'dataset_name': 'Set1',
        'utterance_ids': ["{{utterance_id}}"]
      };
      wordcloud_from_utterances("{{corpus}}", [utterance_set1], waveformVisualizer);

      $('#pt_junk_button').click({'corpus': '{{corpus}}'}, junk_this_pseudoterm);
    });

    $.get("/www/venncloud_template.html", function(data){
      $('#cloud_data_landing_zone').html(data);
    });
  </script>
</head>
<body style="padding-top: 250px;">

<div class="container">
  <nav class="navbar navbar-default navbar-fixed-top" role="navigation">
    <div class="container-fluid">
      <div style="border: 1px solid #C0C0C0; margin-top: 0.5em; margin-bottom: 0.5em;">
        <div id="waveform_visualizer"></div>
      </div>
      <div>
        <div class="form-inline">
          <div class="form-group">
            <span id="pt_snippets_audio_player"></span>
          </div>
          <div class="form-group">
            <label for="pt_eng_display">English</label>
            <input id="pt_eng_display"></input>
          </div>
          <div class="form-group">
            <label for="pt_native_display">Native</label>
            <input id="pt_native_display" disabled></input>
          </div>
          <div class="form-group">
            <button class="btn btn-primary btn-xs" id="pt_junk_button"><i class="glyphicon glyphicon-trash"></i></button>
          </div>
          <div class="form-group">
            <div id="waveform_visualizer_utterance_list" style="padding-left: 1em;"></div>
          </div>
        </div>
      </div>
      <!-- Commented out code below: Experiments replacing existing wordcloud menus
           with Bootstrap-styled wordcloud menus
      -->
      <div style="margin: 0.5em;">
        <div class="btn-group">
          <!--
          <div class="btn-group">
            <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown">
              Common Cloud
              <span class="caret"></span>
            </button>
            <ul class="dropdown-menu" role="menu">
              <table style="width: 300px;">
                <tr>
                  <td style="text-align: center; width: 5%;">
                    -
                  </td>
                  <td style="width: 90%;">
                    <div id='common_cloud_controls'></div>
                  </td>
                  <td style="text-align: center; width: 5%;">
                    +
                  </td>
                </tr>
              </table>
            </ul>
          </div>
          <div class="btn-group">
            <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown">
              TF filter
              <span class="caret"></span>
            </button>
            <ul class="dropdown-menu" role="menu">
              <table style="margin-left: 1em; margin-right: 1em; width: 300px;">
                <tr>
                  <td>
                    <div id='required_observations_slider'></div>
                  </td>
                </tr>
                <tr>
                  <td>
                    Required Times Observed:<span id="required_observations_out"></span>
                  </td>
                </tr>
              </table>
            </ul>
          </div>
          <div class="btn-group">
            <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown">
              IDF filter
              <span class="caret"></span>
            </button>
            <ul class="dropdown-menu" role="menu">
              <table style="margin-left: 1em; margin-right: 1em; width: 300px;">
                <tr>
                  <td>
                    <div id='required_idf_slider'></div>
                  </td>
                </tr>
                <tr>
                  <td>
                    Occurs between <span id="required_idf_out">x</span> documents.
                  </td>
                </tr>
              </table>
            </ul>
          </div>
          -->
          <div class="btn-group">
            <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown">
              Size
              <span class="caret"></span>
            </button>
            <ul class="dropdown-menu" role="menu">
              <table style="margin-left: 1em; margin-right: 1em; width: 400px;">
                <tr>
                  <td style="width: 20%;"><b>Frequency: 0</b></td>
                  <td style="width: 75%;">
                    <div id="size_frequency_slider"></div>
                  </td>
                  <td rowspan="2" style="text-align: center; width: 10%;"><b>+</b></td>
                </tr>
                <tr>
                  <td style="width: 20%;"><b>Rarity: 0</b></td>
                  <td>
                    <div id="size_rarity_slider"></div>
                  </td>
                </tr>
                <tr>
                  <td>Smaller</td>
                  <td>
                    <div id="base_fontsize_slider"></div>
                  </td>
                  <td>Larger</td>
                </tr>
              </table>
            </ul>
          </div>
          <div class="btn-group">
            <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown">
              Opacity
              <span class="caret"></span>
            </button>
            <ul class="dropdown-menu" role="menu">
              <table style="margin-left: 1em; margin-right: 1em; width: 400px;">
                <tr>
                  <td style="width: 20%;"><b>Frequency: <span "text-align: right;">0</span></b></td>
                  <td style="width: 80%;">
                    <div id="opacity_frequency_slider"></div>
                  </td>
                  <td rowspan="2" style="text-align: center; width: 10%;"><b>+</b></td>
                </tr>
                <tr>
                  <td style="width: 20%;"><b>Rarity: <span align=right>0</span></b></td>
                  <td>
                    <div id="opacity_rarity_slider"></div>
                  </td>
                </tr>
                <tr>
                  <td>Light</td>
                  <td>
                    <div id="base_opacity_slider"></div>
                  </td>
                  <td>Dark</td>
                </tr>
              </table>
            </ul>
          </div>
          <div class="btn-group">
            <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown">
              Sort by
              <span class="caret"></span>
            </button>
            <ul class="dropdown-menu" role="menu" style="padding-left: 1em;" id="radio">
              <li>
                <input type="radio" id="ALPHABETIC" name="radio" checked="checked" />
                <label for="ALPHABETIC">Alphabetic</label>
              </li>
              <li>
                <input type="radio" id="COUNT" name="radio" />
                <label for="COUNT">Frequency of Occurence</label>
              </li>
              <li>
                <input type="radio" id="IDF" name="radio" />
                <label for="IDF">Rarity in Corpus</label>
              </li>
            </ul>
          </div>
          <div class="btn-group">
            <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown">
              Legend
              <span class="caret"></span>
            </button>
            <ul class="dropdown-menu" role="menu">
              <div style="margin-left: 1em; margin-right: 1em; width: 400px;">
                <div id="wordcloud_description_output"></div>
              </div>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </nav>

  <div id="wordcloud_landing_zone"></div>

</div><!-- /.container -->

</body>
</html>
