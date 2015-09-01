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
    % for utterance_index in utterance_indices:
    <span class="document_link">
      <a href="../view/{{utterance_index}}">{{str(utterance_index).zfill(4)}}</a>
    </span>
    % end
  </div>

</div><!-- /.container -->

</body>
</html>
