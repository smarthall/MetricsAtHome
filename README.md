MetricsAtHome
=============

To Run

    bin/metricsathome

Make sure that the current working directory is the root of the repository.

This program allows you to use Samsung Photo Displays (other drivers may be
included later) to display metrics and information from various places.

This software depends on:
 - python-suds
 - python-imaging
 - python-dateutil
 - python-simplejson
 - pyusb
 - pyaml

Without an LCD display it also needs
 - wxPython

On a Fedora system to get all these and dependencies do this:

    sudo yum install python-suds python-imaging python-dateutil pyusb PyYAML wxPython python-simplejson

