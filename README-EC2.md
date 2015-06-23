Configuring VaporEngine on EC2
==============================

Create an AWS instance running Red Hat Enterprise Linux (RHEL) 7.1.


Install RHEL packages
----------------------

Install essential packages:

  sudo yum install -y git gcc python-devel wget

Install packages that Craig finds convenient:

  sudo yum install -y emacs-nox screen


Install sox-devel and pysox
---------------------------

Download the CentOS 7 version of the sox-devel package:

  wget http://mirror.centos.org/centos/7/os/x86_64/Packages/sox-devel-14.4.1-6.el7.x86_64.rpm

Install it using:

  sudo yum install -y sox-devel-14.4.1-6.el7.x86_64.rpm 

Create a symbolic link so that easy_install can find the sox.h file:

  ln -s /usr/include/sox/sox.h /usr/include/sox.h

Install pysox:

  sudo easy_install pysox

easy_install will generate some compiler warnings, but these should be
safely ignorable.


Install MongoDB
---------------

The official instructions for installing MongoDB on RHEL can be found here:

  http://docs.mongodb.org/manual/tutorial/install-mongodb-on-red-hat/

Here is the abbreviated version:

Create the file:

  /etc/yum.repos.d/mongodb-org-3.0.repo

which has the contents:

  [mongodb-org-3.0]
  name=MongoDB Repository
  baseurl=https://repo.mongodb.org/yum/redhat/$releasever/mongodb-org/3.0/x86_64/
  gpgcheck=0
  enabled=1

Then installed Mongo using:

  sudo yum install -y mongodb-org
