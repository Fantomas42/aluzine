=======
ALUZINE
=======

Automation of the time stamping, because we are not aluzine.

Installation
============

Install the python package: ::

  $ pip install aluzine

Now the scripts are available.

Configuration
=============

Create a file containing your credentials in this form: ::

  $ cat ~/.aluzine
  [user]
  login: YOURLOGIN
  password: YOURPASSWORD
  domain: http://domain.com

Automation
==========

In ~/.profile add this script to time stamp your arrival when
unlocking your screen: ::

  nohup ./unlock.sh &

In your crontabs add this line, to time stamp your leaving: ::

  0 18 * * 1-5 aluz-out --random-range 20

Now with this configuration, when you login on your workstation,
a time stamp is done, then at night if you have logged in the day
a new time stamp is done for the end of your day.
