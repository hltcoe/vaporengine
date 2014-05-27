<!DOCTYPE html>
<html>
<head>
  <title>ZRL</title>

  <link rel="stylesheet" href="/static/bootstrap-3.1.1/css/bootstrap.css"/>
  <link rel="stylesheet" href="/static/bootstrap-3.1.1/css/bootstrap-theme.css"/>
</head>
<body>

  <div class="container">

    <h1>Corpora</h1>
    <ul>
      % for corpus in current_corpora:
      <li><h2>{{corpus}}</h2></li>
      <ul>
        <li>
          <a href="/corpus/{{corpus}}/wordcloud/">Corpus Wordcloud</a>
        </li>
        <li>
          <a href="/corpus/{{corpus}}/document/list/">Corpus Document List</a>
        </li>
      </ul>
      % end
    </ul>

    <hr />
    <!--
    <h3><a href="/www/test_ajax_calls.html">AJAX Test</a></h3>

    <h3><a href="/www/audio_test.html">Audio Test</a></h3>

    <h3><a href="/www/test_pseudoterm_audio.html">Pseudoterm Audio Test</a></h3>

    <h3><a href="/www/test_cloud_data_call.html">Venncloud data call test</a></h3>
    -->
    <h3><a href="/www/test_venncloud.html">Venncloud display test</a></h3>

    <h3><a href="/www/test_bootstrap_venncloud.html">Venncloud display test - Bootstrap version</a></h3>

  </div><!-- /.container -->
</body>
</html>
