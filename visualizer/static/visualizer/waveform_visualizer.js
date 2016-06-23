
/* global WaveSurfer */

/**
 * @constructor
 * @param {String} visualizerID - DOM ID for element this instance will be attached to
 * @param {Object} customWavesurferSettings - Settings for Wavesurfer instance
 * @param {Object} customSettings - Settings for this WaveformVisualizer instance
 */
function WaveformVisualizer(visualizerID, customWavesurferSettings, customSettings) {
  // Use 'self' to give event handler access to current instance ('this')
  var self = this;

  var combinedWavesurferSettings, defaultWavesurferSettings;
  var defaultSettings;

  // Public member variables
  this.audio_fragments = [];
  this.visualizerID = visualizerID;
  this.wavesurfer = Object.create(WaveSurfer);

  // Initialization
  defaultWavesurferSettings = {
    container: document.querySelector('#' + this.visualizerID),
    dragSelection: false,
    normalize: true,
    progressColor: 'red',
    waveColor: 'pink',
  };
  combinedWavesurferSettings = $.extend({}, defaultWavesurferSettings, customWavesurferSettings);
  this.wavesurfer.init(combinedWavesurferSettings);
  this.wavesurfer.on('region-in', function(marker) {
    updateActiveDocumentForAudioFragment(marker);
  });

  defaultSettings = {
    controlsResizeCallback: undefined
  };
  this.settings = $.extend({}, defaultSettings, customSettings);

  // When browser window size changes, the GUI controls may also change in size
  $(window).resize(function() { callControlsResizeCallback(); });


  //// Public API

  /** Attach a Play/Pause button to DOM element
   * @param {HTMLElement} parentElement - DOM ID of element to attach controls to
   */
  this.addControls = function(parentElement) {
    var playerDiv = $('<div>')
      .attr('id', this.visualizerID + '_audio_control')
      .addClass('audio_control');

    var playPauseButton = $('<button>')
      .addClass('btn btn-primary btn-xs')
      .click(self.playPause)
      .html('<i class="glyphicon glyphicon-play"></i> / <i class="glyphicon glyphicon-pause"></i>');

    playerDiv.append(playPauseButton);

    parentElement.append(playerDiv);
  };

  /** Attach a Play/Pause button to DOM element and load a WAV file from a URL
   * @param {HTMLElement} parentElement - DOM ID of element to attach controls to
   * @param {String} audioSourceURL
   */
  this.addControlsAndLoadAudio = function(parentElement, audioSourceURL) {
    var playerDiv = $('<div>')
      .attr('id', self.visualizerID + '_audio_control')
      .addClass('audio_control');

    var playPauseButton = $('<button>')
      .addClass('btn btn-primary btn-xs')
      .click(self.playPause)
      .html('<i class="glyphicon glyphicon-play"></i> / <i class="glyphicon glyphicon-pause"></i>');

    playerDiv.append(playPauseButton);

    parentElement.append(playerDiv);

    this.loadURL(audioSourceURL);
  };

  /** Remove UI information about current audio clip
   */
  this.clear = function() {
    self.wavesurfer.seekTo(0.0);
    self.wavesurfer.empty();

    // If this WaveformVisualizer instance has an associated <div> that
    // contains buttons linking to source documents (documents), remove
    // the buttons when we clear the waveform.
    var documentListDiv = $('#' + self.visualizerID + '_document_list');
    if (documentListDiv.length > 0) {
      // Delete existing buttons
      documentListDiv.html('');
      callControlsResizeCallback();
    }
  };

  /** Load an audio file from a URL and start playing the file
   * @param {String} audioSourceURL
   */
  this.loadAndPlayURL = function(audioSourceURL) {
    this.loadURL(audioSourceURL);
    this.wavesurfer.on('ready', function() {
      self.wavesurfer.play();
    });
  };

  /** Load an audio file from a URL
   * @param {String} audioSourceURL
   */
  this.loadURL = function(audioSourceURL) {
    var corpus_id, i, term_id;

    this.wavesurfer.load(audioSourceURL);

    // If audio clip is a term audio clip composed of multiple audio events,
    // add markers to waveform at audio event boundaries
    var matches = /(\d+)\/term\/(\d+).wav/g.exec(audioSourceURL);
    if (matches) {
      corpus_id = matches[1];
      term_id = matches[2];

      $.getJSON('/visualizer/' + corpus_id + '/term/' + term_id + "_audio_fragments.json", function(audio_fragments) {
        updateAudioFragments(corpus_id, audio_fragments);
      });
    }
  };

  this.play = function() {
    rewindIfNecessary();
    self.wavesurfer.play();
  };

  this.pause = function() {
    self.wavesurfer.pause();
  };

  this.playPause = function() {
    rewindIfNecessary();
    self.wavesurfer.playPause();
  };


  //// Private functions, some of which are event handlers

  var callControlsResizeCallback = function() {
    if (self.settings.controlsResizeCallback) {
      self.settings.controlsResizeCallback();
    }
  };

  var formatDocumentIndex = function(documentIndex, size) {
    var s = documentIndex+"";
    while (s.length < size) {
      s = "0" + s;
    }
    return s;
  };

  var resetActiveDocumentButtons = function() {
    var
      i,
      totalButtons,
      documentID;

    totalButtons = self.audio_fragments.length;
    for (i = 0; i < totalButtons; i++) {
      documentID = self.audio_fragments[i].document_id;
      $('#' + documentID + '_document_button')
        .addClass('btn-default')
        .removeClass('btn-info');
    }
  };

  var rewindIfNecessary = function() {
    // If waveform progress indicator is at end of clip, move progress
    // indicator back to beginning of clip
    if (Math.abs(self.wavesurfer.getDuration() - self.wavesurfer.getCurrentTime()) < 0.01) {
      resetActiveDocumentButtons();
      self.wavesurfer.seekTo(0.0);
    }
  };

  /** Callback function invoked by WaveSurfer when audio playback reaches marker
   * @callback
   * @param {Object} marker
   */
  var updateActiveDocumentForAudioFragment = function(marker) {
    var
      previousDocumentID = -1,
      documentID;

    // TODO: More sanity checks to verify that this handler is responsible for this region
    if (!self.audio_fragments[marker.id]) {
      return;
    }

    documentID = self.audio_fragments[marker.id].document_id;
    if (parseInt(marker.id) > 0) {
      previousDocumentID = self.audio_fragments[parseInt(marker.id) - 1].document_id;
    }
    if (documentID !== previousDocumentID && previousDocumentID !== -1) {
      $('#' + previousDocumentID + '_document_button')
        .addClass('btn-default')
        .removeClass('btn-info');
    }
    $('#' + documentID + '_document_button')
      .addClass('btn-info')
      .removeClass('btn-default');
  };

  /** Update UI with info about fragments associated with current audio clip.
   *  Add markers for each audio fragment to WaveSurfer instance that
   *  will be called when audio playback enters marker region.
   * @callback
   * @param {String} corpus
   * @param {Array} audio_fragments
   */
  var updateAudioFragments = function(corpus, audio_fragments) {
    var
      audio_fragments_per_document_id = {},
      audio_identifier_for_document_id = {},
      i,
      total_duration = 0.0,
      document_id,
      document_index_for_document_id = {},
      documentListDiv,
      documentSpan;

    self.audio_fragments = audio_fragments;
    self.wavesurfer.clearMarks();
    self.wavesurfer.clearRegions();

    for (i = 0; i < self.audio_fragments.length; i++) {
      self.wavesurfer.region({
        'color': 'blue',
        'id': i,
        'startPosition': total_duration,
        'endPosition': total_duration + self.audio_fragments[i].duration/100.0 - 0.01
      });
      total_duration += self.audio_fragments[i].duration / 100.0;
      self.wavesurfer.mark({
          'color': 'black',
          'id': i,
          'position': total_duration
      });

      document_id = self.audio_fragments[i].document_id;
      if (typeof(audio_fragments_per_document_id[document_id]) === 'undefined') {
        audio_fragments_per_document_id[document_id] = 0;
      }
      audio_fragments_per_document_id[document_id] += 1;
      audio_identifier_for_document_id[document_id] = self.audio_fragments[i].audio_identifier;
      document_index_for_document_id[document_id] = self.audio_fragments[i].document_index;
    }

    documentListDiv = $('#' + self.visualizerID + '_document_list');
    // Delete existing buttons
    documentListDiv.html('');
    // Add buttons for each distinct document
    for (document_id in audio_fragments_per_document_id) {
      documentSpan = $('<a>')
        .addClass('btn btn-default btn-xs')
        .attr('id', document_id + '_document_button')
        .attr('href', '/visualizer/' + corpus +'/document/' + document_index_for_document_id[document_id])
        .attr('role', 'button')
        .attr('style', 'margin-left: 0.5em; margin-right: 0.5em;')
        .html(formatDocumentIndex(document_index_for_document_id[document_id], 4) +
              ' <b>(x' + audio_fragments_per_document_id[document_id] + ')</b>');
      documentListDiv.append(documentSpan);
    }

    callControlsResizeCallback();
  };
}
