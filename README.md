VaporEngine
===========

VaporEngine is a web application that allows users to explore an audio
corpus by listening to and annotating similiar-sounding audio-snippets
called "(Pseudo)Terms".


Requirements
============

* Python 2.7
* The SoX (Sound eXchange) audio library:
  http://sox.sourceforge.net
* The Python packages listed in 'requirements.txt', including:
  * Django - https://www.djangoproject.com
  * pysox - https://pythonhosted.org/pysox/
* An audio corpora that has been run through Aren Jansen's Zero Resource pipeline:
  https://github.com/arenjansen/ZRTools


Installing Requirements
=======================

If you have the pip package manager installed, you can install the
Python packages listed in 'requirements.txt' using the command:

    pip install -r requirements.txt

The steps for installing SoX and pysox will depend on your platform.
Here are instructions for several different platforms:


Installing SoX and pysox - on Ubuntu
------------------------------------

Install the Python development libraries using:

    sudo apt-get install python-dev

Install the SoX development libraries using:

    sudo apt-get install libsox-dev

Install pysox using:

    sudo easy_install pysox

easy_install will generate some compiler warnings, but these should be
safely ignorable.


Installing SoX and pysox - on RHEL on EC2
-----------------------------------------

These instructions are for an Amazon Web Services (AWS) instance of
Red Hat Enterprise Linux (RHEL) 7.1.

Install the Python development libraries using:

    sudo yum install -y python-devel

Download the CentOS 7 version of the `sox-devel` package:

    wget http://mirror.centos.org/centos/7/os/x86_64/Packages/sox-devel-14.4.1-6.el7.x86_64.rpm

Install the downloaded version of `sox-devel` using:

    sudo yum install -y sox-devel-14.4.1-6.el7.x86_64.rpm

Create a symbolic link so that easy_install can find the sox.h file:

    sudo ln -s /usr/include/sox/sox.h /usr/include/sox.h

Install pysox using:

    sudo easy_install pysox

easy_install will generate some compiler warnings, but these should be
safely ignorable.


Installing SoX and pysox - on OS X 10.11
----------------------------------------

Install SoX using the Homebrew package manager (http://brew.sh):

    brew install sox

Install pysox using:

    export CFLAGS=-I/usr/local/include
    export LDFLAGS=-L/usr/local/lib
    easy_install pysox

easy_install will generate some compiler warnings, but these should be
safely ignorable.


Configuring VaporEngine
=======================

Before using VaporEngine for the first time, you will need to create
the VaporEngine database file (`db.sqlite3`) using the command:

    ./manage.py migrate


Importing ZRTools data
======================

ZRTools data format
-------------------

When the ZRTools tool is used to analyze an audio corpus, the tool
will generate multiple output files.  VaporEngine uses the data from
three ZRTools files:

* **files.lst** - A text file with the names of all of the audio source
  files in the corpus

* **matches/master_graph.nodes** - "Pseudoterm" tokens, one per line;
  one per line; the first three columns specify the input file, start
  frame, and end frame (frames = seconds*100)

* **matches/master_graph.dedups** - "Pseudoterm" cluster definitions,
  one line per cluster, each consisting of a list of node IDs that
  corresponds to the line number in the .nodes file

Importing ZRTools data
----------------------

ZRTools data can be imported into VaporEngine by running the
`zrtools_import` command with these parameters:

    ./manage.py zrtools_import CORPUS_NAME PATH_TO_ZRTOOLS_OUTPUT

e.g.:

    ./manage.py zrtools_import DAPS ~/zr_datasets/daps


Running VaporEngine
===================

The VaporEngine server is started using the command:

    ./manage.py runserver

which will start a web server on your local machine that is listening
on port 8000.

You can interact with VaporEngine by pointing your browser at the URL:

  http://localhost:8000
