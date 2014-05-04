

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
