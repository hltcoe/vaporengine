// Global hash mapping DOM ID's of waveform widgets to instances of Waveform class
// TODO: Do something less hacky than a global variable
var widgets = {}


function addControlsForWaveformWidget(parentElement, playerElementID, audioSourceURL) {
  var playerDiv = $('<div>')
    .attr('id', playerElementID + '_audio_control')
    .addClass('audio_control');

  var playPauseButton = $('<button>')
    .addClass('btn btn-primary btn-xs')
    .click(
      {
        'audioSourceURL': audioSourceURL,
        'playerElementID': playerElementID,
      },
      function(event) {
        var widget = widgets[event.data.playerElementID];
        if (widget.url === undefined || widget.url != event.data.audioSourceURL) {
          // Load specified audio file IFF it is not already loaded
          waveformWidgetLoadAndPlayURL(event.data.playerElementID, event.data.audioSourceURL);
          widget.url = event.data.audioSourceURL;
        }
        else {
          waveformWidgetPlayPause(event.data.playerElementID);
        }
      }
    )
    .html('<i class="glyphicon glyphicon-play"></i> / <i class="glyphicon glyphicon-pause"></i>');

  playerDiv.append(playPauseButton);

  parentElement.append(playerDiv);
}

function addWaveformWidget(playerElementID) {
  widgets[playerElementID] = {}
  widgets[playerElementID].wavesurfer = Object.create(WaveSurfer);

  widgets[playerElementID].wavesurfer.init({
    container: document.querySelector('#' + playerElementID),
    normalize: true,
    progressColor: 'purple',
    waveColor: 'violet',
  });
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

function waveformWidgetLoadAndPlayURL(playerElementID, audioSourceURL) {
  waveformWidgetLoadURL(playerElementID, audioSourceURL);
  widgets[playerElementID].wavesurfer.on('ready', function() { widgets[playerElementID].wavesurfer.play(); });
}

function waveformWidgetLoadURL(playerElementID, audioSourceURL) {
  widgets[playerElementID].wavesurfer.load(audioSourceURL);
}

function waveformWidgetPlay(playerElementID) {
  widgets[playerElementID].wavesurfer.play();
}

function waveformWidgetPlayPause(playerElementID) {
  widgets[playerElementID].wavesurfer.playPause();
}

function waveformWidgetPause(playerElementID) {
  widgets[playerElementID].wavesurfer.pause();
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
