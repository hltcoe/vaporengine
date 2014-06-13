<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="/static/jquery-ui-1.10.4/css/ui-lightness/jquery-ui-1.10.4.css"/>
  <link rel="stylesheet" href="/static/bootstrap-3.1.1/css/bootstrap.css"/>
  <link rel="stylesheet" href="/static/bootstrap-3.1.1/css/bootstrap-theme.css"/>

  <link rel="stylesheet" href="/www/dynamic_wordclouds.css">

  <script src="/static/jquery-1.11.1.min.js"></script>
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
      <a href="../view/{{audio_identifier}}">{{audio_identifier}}</a>
    </span>
    % end
  </div>

</div><!-- /.container -->

</body>
</html>
