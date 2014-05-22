// Global hash mapping DOM ID's of waveform visualizers to instances of Wavesurfer class
// TODO: Do something less hacky than a global variable
var visualizers = {};


function addControlsForWaveformVisualizer(parentElement, visualizerID) {
  var playerDiv = $('<div>')
    .attr('id', visualizerID + '_audio_control')
    .addClass('audio_control');

  var playPauseButton = $('<button>')
    .addClass('btn btn-primary btn-xs')
    .click(
      {
        'visualizerID': visualizerID,
      },
      function(event) {
        waveformVisualizerPlayPause(event.data.visualizerID);
      }
    )
    .html('<i class="glyphicon glyphicon-play"></i> / <i class="glyphicon glyphicon-pause"></i>');

  playerDiv.append(playPauseButton);

  parentElement.append(playerDiv);
}

function addControlsAndLoadAudioForWaveformVisualizer(parentElement, visualizerID, audioSourceURL) {
  var playerDiv = $('<div>')
    .attr('id', visualizerID + '_audio_control')
    .addClass('audio_control');

  var playPauseButton = $('<button>')
    .addClass('btn btn-primary btn-xs')
    .click(
      {
        'audioSourceURL': audioSourceURL,
        'visualizerID': visualizerID,
      },
      function(event) {
        waveformVisualizerPlayPause(event.data.visualizerID);
      }
    )
    .html('<i class="glyphicon glyphicon-play"></i> / <i class="glyphicon glyphicon-pause"></i>');

  playerDiv.append(playPauseButton);

  parentElement.append(playerDiv);

  waveformVisualizerLoadURL(visualizerID, audioSourceURL);
}

function addWaveformVisualizer(visualizerID) {
  visualizers[visualizerID] = {};

  visualizers[visualizerID].audio_events = [];

  visualizers[visualizerID].wavesurfer = Object.create(WaveSurfer);

  visualizers[visualizerID].wavesurfer.init({
    container: document.querySelector('#' + visualizerID),
    dragSelection: false,
    normalize: true,
    progressColor: 'red',
    waveColor: 'pink',
  });

  visualizers[visualizerID].wavesurfer.on('region-in', function(marker) {
    updateActiveDocumentForAudioEvent(visualizerID, marker);
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

function resetActiveDocumentButtons(visualizerID) {
  var
    i,
    totalButtons,
    utteranceID;

  totalButtons = visualizers[visualizerID].audio_events.length;
  for (i = 0; i < totalButtons; i++) {
    utteranceID = visualizers[visualizerID].audio_events[i].utterance_id['$oid'];
    $('#' + utteranceID + '_utterance_button')
          .addClass('btn-default')
          .removeClass('btn-info');
  }
}

function updateActiveDocumentForAudioEvent(visualizerID, marker) {
  var
    previousUtteranceID = -1,
    utteranceID;

  // TODO: More sanity checks to verify that this handler is responsible for this region
  if (!visualizers[visualizerID].audio_events[marker.id]) {
    return;
  }

  utteranceID = visualizers[visualizerID].audio_events[marker.id].utterance_id['$oid'];
  if (parseInt(marker.id) > 0) {
    previousUtteranceID = visualizers[visualizerID].audio_events[parseInt(marker.id) - 1].utterance_id['$oid'];
  }
  if (utteranceID != previousUtteranceID && previousUtteranceID != -1) {
    $('#' + previousUtteranceID + '_utterance_button')
          .addClass('btn-default')
          .removeClass('btn-info');
  }
  $('#' + utteranceID + '_utterance_button')
        .addClass('btn-info')
        .removeClass('btn-default');
}

function waveformVisualizerLoadAndPlayURL(visualizerID, audioSourceURL) {
  waveformVisualizerLoadURL(visualizerID, audioSourceURL);
  visualizers[visualizerID].wavesurfer.on('ready', function() {
      visualizers[visualizerID].wavesurfer.play();
  });
}

function waveformVisualizerLoadURL(visualizerID, audioSourceURL) {
  var corpus, i, pseudotermID;

  visualizers[visualizerID].wavesurfer.load(audioSourceURL);

  // If audio clip is a pseudoterm audio clip composed of multiple audio events,
  // add markers to waveform at audio event boundaries
  i = audioSourceURL.indexOf("/audio/pseudoterm/");
  if (i != -1) {
    corpus = audioSourceURL.substr(8, i - 8);
    // Assumes that pseudotermID is a 24 character string
    pseudotermID = audioSourceURL.substr(i + 18, 24);
    $.getJSON('/corpus/' + corpus +"/audio/pseudoterm/" + pseudotermID + "_audio_events.json", function(audio_events) {
      waveformVisualizerUpdateAudioEvents(visualizerID, corpus, audio_events);
    });
  }
}

function waveformVisualizerPlay(visualizerID) {
  waveformVisualizerRewindIfNecessary(visualizerID);
  visualizers[visualizerID].wavesurfer.play();
}

function waveformVisualizerPlayPause(visualizerID) {
  waveformVisualizerRewindIfNecessary(visualizerID);
  visualizers[visualizerID].wavesurfer.playPause();
}

function waveformVisualizerPause(visualizerID) {
  visualizers[visualizerID].wavesurfer.pause();
}

function waveformVisualizerRewindIfNecessary(visualizerID) {
  // If waveform progress indicator is at end of clip, move progress
  // indicator back to beginning of clip
  var ws = visualizers[visualizerID].wavesurfer;

  if (Math.abs(ws.getDuration() - ws.getCurrentTime()) < 0.01) {
    resetActiveDocumentButtons(visualizerID);
    ws.seekTo(0.0);
  }
}

function waveformVisualizerUpdateAudioEvents(visualizerID, corpus, audio_events) {
  var
    audio_events_per_utterance_id = {},
    audio_identifier_for_utterance_id = {},
    i,
    total_duration = 0.0,
    utterance_id,
    utteranceListDiv,
    utteranceSpan;

  visualizers[visualizerID].wavesurfer.clearMarks();
  visualizers[visualizerID].wavesurfer.clearRegions();
  visualizers[visualizerID].audio_events = audio_events;

  for (i in audio_events) {
    visualizers[visualizerID].wavesurfer.region({
      'color': 'blue',
      'id': i,
      'startPosition': total_duration,
      'endPosition': total_duration + audio_events[i].duration/100.0 - 0.01
    });
    total_duration += audio_events[i].duration / 100.0;
    visualizers[visualizerID].wavesurfer.mark({
        'color': 'black',
        'id': i,
        'position': total_duration
    });

    utterance_id = audio_events[i].utterance_id['$oid'];
    if (typeof(audio_events_per_utterance_id[utterance_id]) == 'undefined') {
      audio_events_per_utterance_id[utterance_id] = 0;
    }
    audio_events_per_utterance_id[utterance_id] += 1;
    audio_identifier_for_utterance_id[utterance_id] = audio_events[i].audio_identifier;
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
}


// Adds a <div> containing Pause and Play controls to an element.
//   - parentElement:   DOM element that the <div> will be appended to
//   - playerElementID: unique ID that will be used for creating
//                      DOM ID's assigned to audio player and buttons
//   - audioSourceURL:  URL of audio source file

function addControlsForPlayer(parentElement, playerElementID, audioSourceURL) {
  var controlDiv = $('<div>')
    .attr('id', playerElementID + '_audio_control')
    .addClass('audio_control');
  var audioElement = $('<audio>')
    .attr('id', playerElementID + '_audio_element')
    .bind('ended', {'playerElementID': playerElementID}, function(event) {
      $('#' + event.data.playerElementID + '_play_button').prop('disabled', false);
      $('#' + event.data.playerElementID + '_pause_button').prop('disabled', true);
     });
  var playButton = $('<button>')
    .attr('id', playerElementID + '_play_button')
    .click({'audioSourceURL': audioSourceURL, 'playerElementID': playerElementID}, function(event) {
      var mediaElement = document.getElementById(event.data.playerElementID + '_audio_element');
      mediaElement.src = event.data.audioSourceURL;
      // load() must be called after updating src
      mediaElement.load();
      mediaElement.play();

      $('#' + event.data.playerElementID + '_play_button').prop('disabled', true);
      $('#' + event.data.playerElementID + '_pause_button').prop('disabled', false);
    })
    .html('Play');
  var pauseButton = $('<button>')
    .attr('id', playerElementID + '_pause_button')
    .click({'playerElementID': playerElementID}, function(event) {
      var mediaElement = document.getElementById(event.data.playerElementID + '_audio_element');
      mediaElement.pause();

      $('#' + event.data.playerElementID + '_play_button').prop('disabled', false);
      $('#' + event.data.playerElementID + '_pause_button').prop('disabled', true);
    })
    .html('Pause')
    .prop('disabled', true);

  controlDiv.append(audioElement);
  controlDiv.append(playButton);
  controlDiv.append(pauseButton);

  parentElement.append(controlDiv);
}
