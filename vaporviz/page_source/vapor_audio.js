
function WaveformVisualizer(visualizerID) {

  // Public member variables
  this.audio_events = [];
  this.visualizerID = visualizerID;
  this.wavesurfer = Object.create(WaveSurfer);

  // Private variables with closure scope - used by event handlers, which
  // don't have access to 'this'
  var closure_audio_events = this.audio_events;
  var closure_wavesurfer = this.wavesurfer;

  // Initialization
  this.wavesurfer.init({
    container: document.querySelector('#' + this.visualizerID),
    dragSelection: false,
    normalize: true,
    progressColor: 'red',
    waveColor: 'pink',
  });
  this.wavesurfer.on('region-in', function(marker) {
    updateActiveDocumentForAudioEvent(marker);
  });


  //// Public API

  this.addControls = function(parentElement) {
    var playerDiv = $('<div>')
      .attr('id', this.visualizerID + '_audio_control')
      .addClass('audio_control');

    var playPauseButton = $('<button>')
      .addClass('btn btn-primary btn-xs')
      .click(this.playPause)
      .html('<i class="glyphicon glyphicon-play"></i> / <i class="glyphicon glyphicon-pause"></i>');

    playerDiv.append(playPauseButton);

    parentElement.append(playerDiv);
  };

  this.addControlsAndLoadAudio = function(parentElement, audioSourceURL) {
    var playerDiv = $('<div>')
      .attr('id', this.visualizerID + '_audio_control')
      .addClass('audio_control');

    var playPauseButton = $('<button>')
      .addClass('btn btn-primary btn-xs')
      .click(this.playPause)
      .html('<i class="glyphicon glyphicon-play"></i> / <i class="glyphicon glyphicon-pause"></i>');

    playerDiv.append(playPauseButton);

    parentElement.append(playerDiv);

    loadURL(audioSourceURL);
  };

  this.loadAndPlayURL = function(audioSourceURL) {
    this.loadURL(audioSourceURL);
    this.wavesurfer.on('ready', function() {
      closure_wavesurfer.play();
    });
  };

  this.loadURL = function(audioSourceURL) {
    var corpus, i, pseudotermID, updateCallback, wavesurfer;

    this.wavesurfer.load(audioSourceURL);

    // If audio clip is a pseudoterm audio clip composed of multiple audio events,
    // add markers to waveform at audio event boundaries
    i = audioSourceURL.indexOf("/audio/pseudoterm/");
    if (i != -1) {
      corpus = audioSourceURL.substr(8, i - 8);
      // Assumes that pseudotermID is a 24 character string
      pseudotermID = audioSourceURL.substr(i + 18, 24);

      $.getJSON('/corpus/' + corpus +"/audio/pseudoterm/" + pseudotermID + "_audio_events.json", function(audio_events) {
        updateAudioEvents(corpus, audio_events);
      });
    }
  };

  this.play = function() {
    rewindIfNecessary();
    this.wavesurfer.play();
  };

  this.pause = function() {
    this.wavesurfer.pause();
  };

  this.playPause = function() {
    rewindIfNecessary();
    this.wavesurfer.playPause();
  };


  //// Private functions, some of which are event handlers

  var resetActiveDocumentButtons = function() {
    var
      i,
      totalButtons,
      utteranceID;

    totalButtons = closure_audio_events.length;
    for (i = 0; i < totalButtons; i++) {
      utteranceID = closure_audio_events[i].utterance_id['$oid'];
      $('#' + utteranceID + '_utterance_button')
        .addClass('btn-default')
        .removeClass('btn-info');
    }
  };

  var rewindIfNecessary = function() {
    // If waveform progress indicator is at end of clip, move progress
    // indicator back to beginning of clip
    if (Math.abs(closure_wavesurfer.getDuration() - closure_wavesurfer.getCurrentTime()) < 0.01) {
      resetActiveDocumentButtons();
      closure_wavesurfer.seekTo(0.0);
    }
  };

  var updateActiveDocumentForAudioEvent = function(marker) {
    var
      previousUtteranceID = -1,
      utteranceID;

    // TODO: More sanity checks to verify that this handler is responsible for this region
    if (!closure_audio_events[marker.id]) {
      return;
    }

    utteranceID = closure_audio_events[marker.id].utterance_id['$oid'];
    if (parseInt(marker.id) > 0) {
      previousUtteranceID = closure_audio_events[parseInt(marker.id) - 1].utterance_id['$oid'];
    }
    if (utteranceID != previousUtteranceID && previousUtteranceID != -1) {
      $('#' + previousUtteranceID + '_utterance_button')
        .addClass('btn-default')
        .removeClass('btn-info');
    }
    $('#' + utteranceID + '_utterance_button')
      .addClass('btn-info')
      .removeClass('btn-default');
  };

  var updateAudioEvents = function(corpus, audio_events) {
    var
      audio_events_per_utterance_id = {},
      audio_identifier_for_utterance_id = {},
      i,
      total_duration = 0.0,
      utterance_id,
      utteranceListDiv,
      utteranceSpan;

    closure_audio_events = audio_events;
    closure_wavesurfer.clearMarks();
    closure_wavesurfer.clearRegions();

    for (i in closure_audio_events) {
      closure_wavesurfer.region({
        'color': 'blue',
        'id': i,
        'startPosition': total_duration,
        'endPosition': total_duration + closure_audio_events[i].duration/100.0 - 0.01
      });
      total_duration += closure_audio_events[i].duration / 100.0;
      closure_wavesurfer.mark({
          'color': 'black',
          'id': i,
          'position': total_duration
      });

      utterance_id = closure_audio_events[i].utterance_id['$oid'];
      if (typeof(audio_events_per_utterance_id[utterance_id]) == 'undefined') {
        audio_events_per_utterance_id[utterance_id] = 0;
      }
      audio_events_per_utterance_id[utterance_id] += 1;
      audio_identifier_for_utterance_id[utterance_id] = closure_audio_events[i].audio_identifier;
    }

    utteranceListDiv = $('#' + visualizerID + '_utterance_list');
    // Delete existing buttons
    utteranceListDiv.html('');
    // Add buttons for each distinct utterance
    for (utterance_id in audio_events_per_utterance_id) {
      utteranceSpan = $('<a>')
        .addClass('btn btn-default btn-xs')
        .attr('id', utterance_id + '_utterance_button')
        .attr('href', '/corpus/' + corpus +'/document/view/' + audio_identifier_for_utterance_id[utterance_id])
        .attr('role', 'button')
        .attr('style', 'margin-left: 0.5em; margin-right: 0.5em;')
        .html(audio_identifier_for_utterance_id[utterance_id] +
              ' <b>(x' + audio_events_per_utterance_id[utterance_id] + ')</b>');
      utteranceListDiv.append(utteranceSpan);
    }
  };
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
