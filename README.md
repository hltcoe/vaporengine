VaporEngine
===========

VaporEngine is a web application that allows users to explore an audio
corpus by listening to and annotating Pseudoterms.


Requirements
------------

* An audio corpora that has been run through Aren Jansen's Zero Resource pipeline
* A MongoDB server running MongoDB v2.0.2 or higher
* Python 2.7
* The Python packages listed in 'requirements.txt', which can be installed
  using the pip package manager by running the command:

    ```bash
    pip install -r requirements.txt
    ```


Configuring VaporEngine
-----------------------

Configure the MongoDB server settings and ZR filepaths by editing the
file ```settings.py```.  Here is a sample configuration for the
'buckeye' corpora:

```python
buckeye = {}
buckeye['DB_HOST'] = 'r4n7'
buckeye['DB_NAME'] = 'buckeye'
buckeye['DB_PORT'] = 27017
buckeye['SOX_SIGNAL_INFO'] = pysox.CSignalInfo(16000.0,1,16)
buckeye['ZR_CLUSTERS'] = 'matches/master_graph.dedups.80'
buckeye['ZR_PATH'] = '/home/hltcoe/ajansen/discovery/exp/buckeye-T25/'
settings['buckeye'] = buckeye
```

If you're not certain what SOX_SIGNAL_INFO parameters to use for your
audio source files, you can run the command:

```bash
soxi AUDIO_SOURCE_FILE
```

which will print out information about the format of your audio files,
including the Sample Rate (for the 'buckeye' example, the rate is
16000), number of Channels (1), and Precision (16 bits).

Update the ```current_corpora``` variable at the end of the file:

```python
current_corpora = ['buckeye', 'fisher_spanish', 'QASW', 'tagalog']
```

so that the list only contains the names of locally installed corpora.


Importing ZR data into MongoDB
------------------------------

Run the script:

```bash
./vaporgasp/vapor_inhaler.py DATASET_NAME
```

where DATASET_NAME is the name of one of the ZR datasets specified in
```settings.py```.


Running the server
------------------

Run the script:

```bash
./bin/start_webserver.sh
```

This command will start a Bottle webserver, which by default will
listen on port 12321.  Open this URL in your browser:

  http://localhost:12321

to view the VaporEngine demo running on your machine.


Backing up and Restoring Annotations
------------------------------------

The scripts ```vaporgasp/backup_annotations.py```
and ```vaporgasp/restore_annotations.py``` can be used to backup and
restore VaporEngine annotations.  The annotations will be saved to a
TSV file with two columns:

1. the Pseudoterm ID assigned by the ZR system
2. the text annotation for this Pseudoterm ID
