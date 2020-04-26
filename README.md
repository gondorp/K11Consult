K11Consult
==========

A python project that uses pyserial to interact with the ECU of Nissan vehicles that utilise the Nissan Consult protocol.

The protocol reads and writes hex via a serial connection, with dashboard.py sending the commands and reading in realtime the resultant data stream from the ECU. The script is essentially in two parts; a non blocking deamonised thread that interacts with the ECU, and a gui using pygame that displays the data in the style of a dashboard. There are no external images used as I've written this for minimal CPU usage and to show what's possible using the inbuilt drawing functions of pygame. A YouTube video can be [found here](http://youtu.be/cykgpQZ5iEU) of the program running in both windowed and fullscreen modes.

Run the commands in terminal
group pi

usermod -a -G dialout pi

python dashboard.py

Currently the data displayed is MPH, RPM (large centre arcs), AAC, MAF, temperature and battery voltage. The script is actually streaming 14 data values but these are the most useful to display. Pressing f will make it go fullscreen, w will make it revert back to windowed mode.
