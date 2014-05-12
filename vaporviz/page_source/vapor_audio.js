// Global hash mapping DOM ID's of waveform widgets to instances of Waveform class
// TODO: Do something less hacky than a global variable
var wavesurfers = {};


function addWaveformWidget(playerElementID) {
  wavesurfers[playerElementID] = Object.create(WaveSurfer);

  wavesurfers[playerElementID].init({
    container: document.querySelector('#' + playerElementID),
    waveColor: 'violet',
    progressColor: 'purple'
  });
}

function waveformWidgetLoadAndPlayURL(playerElementID, audioSourceURL) {
  wavesurfers[playerElementID].load(audioSourceURL);
  wavesurfers[playerElementID].on('ready', function() { wavesurfers[playerElementID].play(); });
}

function waveformWidgetLoadURL(playerElementID, audioSourceURL) {
  wavesurfers[playerElementID].load(audioSourceURL);
}

function waveformWidgetPlay(playerElementID) {
  wavesurfers[playerElementID].play();
}

function waveformWidgetPause(playerElementID) {
  wavesurfers[playerElementID].pause();
}

function addControlsForWaveformWidget(parentElement, playerElementID, controlsID, audioSourceURL) {
  var playerDiv = $('<div>')
    .attr('id', playerElementID + '_audio_control')
    .addClass('audio_control');

  var playButton = $('<button>')
    .addClass('btn btn-primary')
    .attr('id', controlsID + '_play_button')
    .click(
        {
            'audioSourceURL': audioSourceURL,
            'controlsID': controlsID,
            'playerElementID': playerElementID,
        },
        function(event) {
            waveformWidgetLoadAndPlayURL(event.data.playerElementID, event.data.audioSourceURL);
            $('#' + event.data.controlsID + '_play_button').prop('disabled', true);
            $('#' + event.data.controlsID + '_pause_button').prop('disabled', false);
        }
    )
    .html('<i class="glyphicon glyphicon-play"></i>Play');
  var pauseButton = $('<button>')
    .addClass('btn btn-primary')
    .attr('id', controlsID + '_pause_button')
    .click(
        {
            'controlsID': controlsID,
            'playerElementID': playerElementID,
        },
        function(event) {
            waveformWidgetPause(event.data.playerElementID);
            $('#' + event.data.controlsID + '_play_button').prop('disabled', false);
            $('#' + event.data.controlsID + '_pause_button').prop('disabled', true);
        }
    )
    .html('<i class="glyphicon glyphicon-pause"></i>Pause')
    .prop('disabled', true);

  playerDiv.append(playButton);
  playerDiv.append(pauseButton);

  parentElement.append(playerDiv);
}



//TODO: split into two separate elements -- one that attaches new buttons, one that calls with new pseudoterm

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


function getURLforAudioEventWAV(audioEventID) {
  return '/audio/audio_event/' + audioEventID + '.wav';
}

function getURLforPseudotermWAV(pseudotermID) {
  return '/audio/pseudoterm/' + pseudotermID + '.wav';
}

function getURLforUtteranceWAV(utteranceID) {
  return '/audio/utterance/' + utteranceID + '.wav';
}
