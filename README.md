
All scripts should be run from the VaporEngine root directory. 
This will (theoretically) make all the path variables be set correctly.
Let the directory this README resides in be $VEHOME

For example:
To start the webserver --
cd $VEHOME
./bin/start_webserver.sh


==Accessing the VaporBottle webserver==
You need an HLTCOE account to be able to access this from our grid.

To access the webserver, once it's running, you may need to create a tunnel from your local
machine to the machine the webserver is running on. For example, if we are running the 
webserver on test2, we call
[you@test2]: cd $VEHOME
[you@test2]: ./bin/start_webserver.sh

In a separate terminal window, establish a tunnel to the proper port (12321 by default) on test2:
[you@local]: ssh -L 12321:test2:12321 you@external.hltcoe.jhu.edu

Now, on your local machine point Firefox [Safari?] at:
http://localhost:12321/www/test.html 

This should give you a simple HTML page returned (from the vapor_bottle.py webserver).
[this (and anything from http://localhost:12321/www/) serves up the page located at 
$VEHOME/vaporviz/page_source/test.html]

