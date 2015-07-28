Configuring VaporEngine on Ubuntu 14.04
=======================================

Install libsox-dev and pysox
----------------------------

Install the sox library using:

    sudo apt-get install libsox-dev

Install the Python development libraries using:

    sudo apt-get install python-dev

Install pysox:

    sudo easy_install pysox

easy_install will generate some compiler warnings, but these should be
safely ignorable.


Install MongoDB
---------------

    sudo apt-get install mongodb


Install pip
-----------

    wget https://bootstrap.pypa.io/get-pip.py

    sudo python get-pip.py
