VaporEngine
===========



Using the VaporEngine demo on test1
-----------------------------------

You must have an HLTCOE account to view the demo on test1.

To view the demo running on test1 from outside the COE firewall, run
this shell script:

```
./create_tunnel_to_test1_demo.sh YOUR_COE_USERNAME
```

which will create an SSH tunnel to the VaporEngine server running on
test1.  Then just point your favorite web browser at:

  http://localhost:12321

to use the VaporEngine demo


Requirements
------------

* An audio corpora that has been run through the ZRL pipeline
* A MongoDB server running MongoDB v2.0.2 or higher
* Python 2.7
* The Python packages listed in 'requirements.txt', which can be installed
  using the pip package manager by running the command:

```
pip install -r requirements.txt
```


Configuring VaporEngine
-----------------------

Configure the MongoDB server settings and ZRL filepaths by editing the
file ```settings.py```.

Update the ```current_corpora``` variable at the end of the file to
list the locally installed corpora.


Importing ZRL data into MongoDB
-------------------------------

Run the script:

```
./vaporgasp/vapor_inhaler.py DATASET_NAME
```

where DATASET_NAME is the name one of the ZRL datasets specified
in ```settings.py```.


Running the server
------------------

Run the script:

```
./bin/start_webserver.sh
```

This command will start a Bottle webserver, which by default will
listen on port 12321.  Open this URL in your browser:

  http://localhost:12321

to view the VaporEngine demo running your machine.


Backing up and Restoring Annotations
------------------------------------

The scripts ```vaporgasp/backup_annotations.py``` and
```vaporgasp/restore_annotations.py``` can be used to backup and
restore VaporEngine annotations.  The annotations will be saved to a
TSV file with two columns:
  * the Pseudoterm ID assigned by the ZRL system
  * the text annotation for this Pseudoterm ID
