<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="/www/jquery-ui.css">
  <link rel="stylesheet" href="/www/dynamic_wordclouds.css">

  <link rel="stylesheet" href="/static/bootstrap-3.1.1/css/bootstrap.css"/>
  <link rel="stylesheet" href="/static/bootstrap-3.1.1/css/bootstrap-theme.css"/>

  <script src="/static/jquery-1.11.0.min.js"></script>
  <script src="/static/bootstrap-3.1.1/js/bootstrap.js"></script>

  <style>
    .document_link {
      margin: 0.5em;
    }
  </style>
</head>
<body>

<div class="container">
  <h2>Document List</h2>
  <div>
    % for audio_identifier in utterance_audio_identifiers:
    <span class="document_link">
      <a href="/document/view/{{audio_identifier}}">{{audio_identifier}}</a>
    </span>
    % end
  </div>

</div><!-- /.container -->

</body>
</html>
